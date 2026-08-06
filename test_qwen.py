import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

MODEL_NAME = "Qwen/Qwen2.5-Coder-3B-Instruct"

print("CUDA Available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0))

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
)

print("\nLoading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="cuda",
)

print("\nModel loaded successfully!")

prompt = "Write a Python function that reverses a linked list."

messages = [
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

inputs = tokenizer(text, return_tensors="pt").to("cuda")

print("Generating...\n")

with torch.inference_mode():
    output = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.2,
    )

answer = tokenizer.decode(
    output[0][inputs.input_ids.shape[1]:],
    skip_special_tokens=True,
)

print(answer)