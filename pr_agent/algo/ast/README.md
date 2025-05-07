# AST-based Code Chunking System

This module provides a system for parsing Python code and chunking it semantically using Abstract Syntax Trees (ASTs). It forms the foundation for the Enhanced Context-Aware PR-Reviewer system, which uses these chunks as the leaf nodes in a Merkle tree for efficient tracking and indexing of code changes.

## Overview

The system consists of three main components:

1. **AST Chunker**: Parses Python code into an AST and extracts meaningful logical units (functions, classes, methods).
2. **Merkle Tree**: A tree data structure that tracks changes in code chunks at a semantic level.
3. **Setup Tools**: Utilities for setting up the required tree-sitter components.

## Setup

Before using the AST chunking system, you need to set up tree-sitter and the Python grammar:

```bash
# Install tree-sitter and set up the Python grammar
python -m pr_agent.algo.setup_tree_sitter
```

This script will:
1. Install the tree-sitter Python package
2. Clone the tree-sitter-python repository
3. Build the Python language library

## Usage

### Chunking Python Code

You can chunk Python code either from a string or from a file:

```python
from pr_agent.algo.ast_chunker import chunk_code_string, chunk_file

# Chunk code from a string
code = """
def hello():
    print("Hello, world!")

class MyClass:
    def method(self):
        return "Result"
"""
chunks = chunk_code_string(code, "example.py")

# Chunk code from a file
file_chunks = chunk_file("path/to/file.py")
```

Each chunk contains the following information:
- `code_string`: The extracted source code
- `type`: The type of chunk ("function", "class", "method")
- `start_line`: The starting line number
- `end_line`: The ending line number
- `path`: The file path
- `doc_id`: A unique identifier generated from the normalized code content

### Using the Merkle Tree

The Merkle tree allows you to efficiently track changes between different versions of the codebase:

```python
from pr_agent.algo.merkle_tree import MerkleTree

# Build a Merkle tree from chunks
tree = MerkleTree().build_from_chunks(chunks)

# Or build directly from a directory
tree = MerkleTree().build_from_directory("path/to/directory", "*.py")

# Compare two trees to find changed chunks
changed_chunk_ids = tree_before.compare(tree_after)
```

## Example

A simple example demonstrating the AST chunking and Merkle tree functionality:

```python
from pr_agent.algo.ast_chunker import chunk_code_string
from pr_agent.algo.merkle_tree import MerkleTree

# Example code before changes
code_before = """
def function_a():
    return "Hello World"

def function_b():
    return "Goodbye World"
"""

# Example code after changes
code_after = """
def function_a():
    return "Hello World"

def function_b():
    return "Farewell World"
"""

# Build Merkle trees
chunks_before = chunk_code_string(code_before, "example.py")
tree_before = MerkleTree().build_from_chunks(chunks_before)

chunks_after = chunk_code_string(code_after, "example.py")
tree_after = MerkleTree().build_from_chunks(chunks_after)

# Find changed chunks
changed_chunk_ids = tree_before.compare(tree_after)
print("Changed chunks:", changed_chunk_ids)
```

## Running Tests

You can run the test module to see the AST chunker in action:

```bash
python -m pr_agent.algo.test_ast_chunker
```

## Integration with RagEngine

In the full implementation, changed chunks will be:
1. Deleted from the RagEngine index if they're outdated
2. Added to the index if they're new or modified

This ensures that the RagEngine always has the most up-to-date semantic understanding of the codebase for PR reviews. 