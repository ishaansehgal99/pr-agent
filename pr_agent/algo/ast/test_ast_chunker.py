"""
Test module for the AST chunker.

This module demonstrates how to use the AST chunker to parse
Python code and extract semantic chunks.
"""

import os
import sys
import json
from typing import List, Dict, Any

from pr_agent.algo.ast_chunker import chunk_code_string, chunk_file, CodeChunk

# Example Python code for testing
EXAMPLE_CODE = """
import os
import sys
from typing import List, Dict, Optional

class MyClass:
    \"\"\"A sample class for demonstrating AST chunking.\"\"\"
    
    def __init__(self, value: int):
        self.value = value
        
    def get_value(self) -> int:
        \"\"\"Return the stored value.\"\"\"
        return self.value
        
    def double_value(self) -> int:
        \"\"\"Double the stored value.\"\"\"
        return self.value * 2

def helper_function(arg1: str, arg2: Optional[int] = None) -> str:
    \"\"\"A top-level helper function.\"\"\"
    print("Processing", arg1)
    if arg2 is not None:
        return f"{arg1} {arg2}"
    return arg1

# Some procedural code that won't be extracted as a chunk
result = helper_function("test", 42)
print(result)
"""

def chunks_to_dict(chunks: List[CodeChunk]) -> List[Dict[str, Any]]:
    """Convert a list of CodeChunk objects to a list of dictionaries for easy printing."""
    return [
        {
            "type": chunk.type,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "code_string": chunk.code_string[:50] + "..." if len(chunk.code_string) > 50 else chunk.code_string,
            "doc_id": chunk.doc_id
        }
        for chunk in chunks
    ]

def main():
    """Main function to demonstrate AST chunking."""
    print("AST Chunking Demo")
    print("----------------")
    
    # Test with code string
    print("\nChunking example code string...")
    chunks = chunk_code_string(EXAMPLE_CODE, "example.py")
    print(f"Found {len(chunks)} chunks:")
    for i, chunk_dict in enumerate(chunks_to_dict(chunks)):
        print(f"\nChunk {i+1}:")
        print(f"Type: {chunk_dict['type']}")
        print(f"Lines: {chunk_dict['start_line']}-{chunk_dict['end_line']}")
        print(f"Doc ID: {chunk_dict['doc_id']}")
        print(f"Code: {chunk_dict['code_string']}")
    
    # Test with current file
    print("\nChunking the current file...")
    current_file = __file__
    file_chunks = chunk_file(current_file)
    print(f"Found {len(file_chunks)} chunks in {os.path.basename(current_file)}:")
    for i, chunk_dict in enumerate(chunks_to_dict(file_chunks)):
        print(f"\nChunk {i+1}:")
        print(f"Type: {chunk_dict['type']}")
        print(f"Lines: {chunk_dict['start_line']}-{chunk_dict['end_line']}")
        print(f"Code: {chunk_dict['code_string']}")

if __name__ == "__main__":
    main() 