from __future__ import annotations

import os
from typing import Literal

import torch
from dotenv import load_dotenv
from groq import Groq
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

load_dotenv()

Backend = Literal["local", "groq"]


class LLM:
    """
    Provides one interface for either:

    1. Local Qwen inference through PyTorch + CUDA
    2. Remote Llama inference through the Groq API
    """

    LOCAL_MODEL_NAME = "Qwen/Qwen2.5-Coder-3B-Instruct"
    GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

    def __init__(self, backend: Backend | None = None) -> None:
        # Default to the environment variable, then local if none is provided.
        """Create an `LLM` instance and initialize the chosen backend.

            The constructor reads the `backend` argument or the `SOCKAI_BACKEND`
            environment variable (defaults to "local") and initializes either
            the local PyTorch/CUDA model or the Groq client.
            """
        selected_backend = backend or os.getenv("SOCKAI_BACKEND", "local")
        selected_backend = selected_backend.strip().lower()

        if selected_backend not in {"local", "groq"}:
            raise ValueError(
                "SOCKAI_BACKEND must be either 'local' or 'groq'."
            )

        self.backend: Backend = selected_backend  # type: ignore[assignment]

        self.groq_client: Groq | None = None
        self.tokenizer = None
        self.model = None

        if self.backend == "local":
            self._initialize_local_model()
        else:
            self._initialize_groq()

    def _initialize_groq(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is missing from the environment."
            )

        self.groq_client = Groq(api_key=api_key)

        print(
            f"LLM backend: Groq API\n"
            f"Model: {self.GROQ_MODEL_NAME}"
        )
        """Initialize the Groq API client.

            Reads `GROQ_API_KEY` from the environment and creates a `Groq`
            client stored in `self.groq_client`. Raises if the API key is
            missing.
            """

    def _initialize_local_model(self) -> None:
        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA is unavailable. Run cuda_test.py using the same "
                "virtual environment that starts SockAI."
            )

        print(
            f"LLM backend: local PyTorch/CUDA\n"
            f"Model: {self.LOCAL_MODEL_NAME}\n"
            f"GPU: {torch.cuda.get_device_name(0)}"
        )

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,

            # Perform calculations in FP16 even though the stored weights
            # are compressed to 4 bits.
            bnb_4bit_compute_dtype=torch.float16,

            # NF4 is generally suitable for neural-network weights.
            bnb_4bit_quant_type="nf4",

            # Apply an additional quantization layer to reduce memory use.
            bnb_4bit_use_double_quant=True,
        )

        print("Loading tokenizer...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.LOCAL_MODEL_NAME,
            local_files_only=True,  # Avoid downloading from the internet
        )

        print("Loading local model into GPU memory...")

        self.model = AutoModelForCausalLM.from_pretrained(
            self.LOCAL_MODEL_NAME,
            quantization_config=quantization_config,

            # Put the model on the first CUDA GPU.
            device_map={"": 0},

            # Avoid unnecessary CPU memory duplication while loading.
            low_cpu_mem_usage=True,
            local_files_only=True,  # Avoid downloading from the internet
        )

        self.model.eval()

        allocated_gb = torch.cuda.memory_allocated(0) / (1024**3)
        reserved_gb = torch.cuda.memory_reserved(0) / (1024**3)

        print("Local model loaded successfully.")
        print(f"Allocated VRAM: {allocated_gb:.2f} GB")
        print(f"Reserved VRAM: {reserved_gb:.2f} GB")
        """Initialize the local PyTorch model on the GPU.

            Verifies CUDA availability, builds a 4-bit quantization config,
            loads the tokenizer and model into GPU memory, switches the model
            to evaluation mode, and prints VRAM usage. This is the expensive
            operation that should be done once at startup.
            """

    def generate_response(self, messages: list[dict[str, str]]) -> str:
        if self.backend == "groq":
            return self._generate_with_groq(messages)

        return self._generate_locally(messages)
        """Generate a response for the supplied chat `messages`.

            Routes the request to the configured backend implementation
            (`_generate_with_groq` or `_generate_locally`) and returns the
            generated text.
            """

    def _generate_with_groq(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        if self.groq_client is None:
            raise RuntimeError("The Groq client was not initialized.")

        response = self.groq_client.chat.completions.create(
            model=self.GROQ_MODEL_NAME,
            messages=messages,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("Groq returned an empty response.")

        return content
        """Use the Groq chat completions API to generate a response.

        Sends the chat `messages` to the remote Groq model and returns
        the first choice's message content. Raises if the client was not
        initialized or the API returns an empty result.
        """

    def _generate_locally(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("The local model was not initialized.")

        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",

            # Start conservatively because your GPU has 6 GB of VRAM.
            truncation=True,
            max_length=4096,
        )

        # Move every input tensor to the same device as the model.
        inputs = {
            name: tensor.to(self.model.device)
            for name, tensor in inputs.items()
        }

        prompt_token_count = inputs["input_ids"].shape[1]

        with torch.inference_mode():
            generated = self.model.generate(
                **inputs,

                # Maximum length of the newly generated answer.
                max_new_tokens=400,

                # Deterministic generation is preferable for coding.
                do_sample=False,

                # Prevent an undefined padding-token warning.
                pad_token_id=self.tokenizer.eos_token_id,
            )

        new_tokens = generated[0, prompt_token_count:]

        response = self.tokenizer.decode(
            new_tokens,
            skip_special_tokens=True,
        ).strip()

        if not response:
            raise RuntimeError("The local model generated an empty response.")

        return response
        """Generate a response locally using the loaded PyTorch model.

        Formats the chat prompt with `tokenizer.apply_chat_template`,
        tokenizes and moves inputs to the model device, runs
        `model.generate` deterministically, decodes the newly generated
        tokens, and returns the resulting string. Raises if the model or
        tokenizer are uninitialized or if generation yields no text.
        """