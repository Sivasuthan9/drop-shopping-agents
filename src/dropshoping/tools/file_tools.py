from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class WriteFileToolInput(BaseModel):
    """Input schema for WriteFileTool."""
    file_path: str = Field(..., description="Path where to save the file")
    content: str = Field(..., description="Content to write to file")


class WriteFileTool(BaseTool):
    name: str = "write_file_tool"
    description: str = (
        "Write text content to a file. Useful for creating markdown reports, "
        "text files, and other plain text outputs."
    )
    args_schema: Type[BaseModel] = WriteFileToolInput

    def _run(self, file_path: str, content: str) -> str:
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully wrote content to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"


class ReadFileToolInput(BaseModel):
    """Input schema for ReadFileTool."""
    file_path: str = Field(..., description="Path to the file to read")


class ReadFileTool(BaseTool):
    name: str = "read_file_tool"
    description: str = (
        "Read the contents of a text file and return as string."
    )
    args_schema: Type[BaseModel] = ReadFileToolInput

    def _run(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"