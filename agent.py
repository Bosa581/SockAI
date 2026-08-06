import tools
from llm import LLM
from pathlib import Path


class Agent:
    def __init__(self,workspace_root):
        self.tools = tools
        self.llm = LLM()
        self.Workspace_Root = Path(workspace_root).resolve()
        self.active_file = []  # Initialize the active file to None
        self.current_file = None  # Initialize the current file to None

        if not self.Workspace_Root.exists():
            raise ValueError(f"Workspace root '{self.Workspace_Root}' does not exist.")

    def _resolve_target_file(self, file_reference, current_file=None):
        if not file_reference:
            return None

        if current_file:
            active_path = Path(current_file)
            if active_path.is_absolute():
                active_dir = active_path.parent
            else:
                active_dir = (self.Workspace_Root / active_path).parent
        else:
            active_dir = self.Workspace_Root

        resolved = self.tools.resolve_path(file_reference, workspace_root=self.Workspace_Root)
        if resolved:
            return resolved

        candidate = (active_dir / file_reference).resolve()
        if candidate.exists():
            return candidate

        return None

    def actions(self, current_file, prompt):
        normalizedprompt = prompt.strip().lower() #converts the prompt to lowercase and removes any leading or trailing whitespace
        if current_file:
            self.current_file = Path(current_file)
        if normalizedprompt.startswith("read file "):
            file_reference = prompt.split("read file ", 1)[1].strip()
            resolved_path = self._resolve_target_file( 
                file_reference, current_file=current_file
            )
            if resolved_path is None: #makes sure that the file exists and is accessible before attempting to read it
                file_content = self.tools.read_file(file_reference, workspace_root=self.Workspace_Root)
            else:
                file_content = self.tools.read_file(str(resolved_path), workspace_root=self.Workspace_Root)
                self.current_file = resolved_path  # Store the file reference for future use
            if resolved_path not in self.active_file:
                self.active_file.append(resolved_path)  # Add the resolved path to the active files list

            messages = [
                {
                    "role": "user",
                    "content": (
                        f"User request:\n{prompt}\n\n" #the prompt is included in the message to provide context for the LLM
                        f"Contents of {file_reference}:\n"
                        f"{file_content}"
                    )
                }
            ]
        else:
            if self.active_file: # If there are active files, read their contents and include them in the message to the LLM

                all_file_contents = ""

                for file_path in self.active_file:
                    file_content = self.tools.read_file(
                        str(file_path),
                        workspace_root=self.Workspace_Root
                )

                    all_file_contents += (
                        f"\n\nContents of {file_path.name}:\n"
                        f"{file_content}"
                    )

                messages = [
                    {
                        "role": "user",
                        "content": (
                            f"User request:\n{prompt}\n\n"
                            f"Current file: {self.current_file.name}\n"
                            f"{all_file_contents}"
                        )
                    }
                ]

            else:
                messages = [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
        return self.llm.generate_response(messages)

