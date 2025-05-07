"""
Merkle tree implementation for tracking code chunks.

This module provides a basic implementation of a Merkle tree that can be used
to track changes in code chunks and efficiently identify which chunks need to be
reindexed when files are modified.
"""

import hashlib
from typing import Dict, List, Optional, Union, Any
import os
from pathlib import Path

from pr_agent.algo.ast_chunker import CodeChunk, chunk_file


class MerkleNode:
    """Represents a node in the Merkle tree."""
    
    def __init__(self, hash_value: str, children: Optional[List['MerkleNode']] = None):
        """
        Initialize a Merkle tree node.
        
        Args:
            hash_value: The hash value of this node.
            children: The children nodes of this node, if any.
        """
        self.hash_value = hash_value
        self.children = children or []
    
    def __eq__(self, other):
        """Check if this node is equal to another node based on hash value."""
        if not isinstance(other, MerkleNode):
            return False
        return self.hash_value == other.hash_value
    
    def is_leaf(self) -> bool:
        """Check if this node is a leaf node (has no children)."""
        return len(self.children) == 0


class MerkleTree:
    """Merkle tree for tracking changes in code chunks."""
    
    def __init__(self):
        """Initialize an empty Merkle tree."""
        self.root = None
        self.chunk_nodes: Dict[str, MerkleNode] = {}  # Maps file paths to leaf nodes
    
    @staticmethod
    def hash_content(content: str) -> str:
        """Hash the given content using SHA-256."""
        return hashlib.sha256(content.encode()).hexdigest()
    
    @staticmethod
    def hash_children(children: List[MerkleNode]) -> str:
        """Compute the hash of a list of child nodes."""
        if not children:
            return ""
        combined = "".join(child.hash_value for child in children)
        return MerkleTree.hash_content(combined)
    
    def build_from_chunks(self, chunks: List[CodeChunk]) -> 'MerkleTree':
        """
        Build a Merkle tree from a list of code chunks.
        
        Args:
            chunks: List of CodeChunk objects representing code chunks.
            
        Returns:
            The Merkle tree instance (self).
        """
        # Group chunks by file path
        path_to_chunks: Dict[str, List[CodeChunk]] = {}
        for chunk in chunks:
            path = chunk.path
            if path not in path_to_chunks:
                path_to_chunks[path] = []
            path_to_chunks[path].append(chunk)
        
        # Create leaf nodes for each chunk
        file_nodes = []
        for path, file_chunks in path_to_chunks.items():
            chunk_nodes = []
            for chunk in file_chunks:
                # Create a leaf node for each chunk
                leaf = MerkleNode(chunk.doc_id)
                chunk_nodes.append(leaf)
                self.chunk_nodes[chunk.doc_id] = leaf
            
            # Create a file node that has all chunks as children
            file_hash = MerkleTree.hash_children(chunk_nodes)
            file_node = MerkleNode(file_hash, chunk_nodes)
            file_nodes.append(file_node)
        
        # Create the root node
        root_hash = MerkleTree.hash_children(file_nodes)
        self.root = MerkleNode(root_hash, file_nodes)
        
        return self
    
    def build_from_directory(self, directory: Union[str, Path], file_pattern: str = "*.py") -> 'MerkleTree':
        """
        Build a Merkle tree from a directory of Python files.
        
        Args:
            directory: The directory to scan for Python files.
            file_pattern: The glob pattern to use for finding files (default: "*.py").
            
        Returns:
            The Merkle tree instance (self).
        """
        chunks = []
        directory_path = Path(directory)
        
        for file_path in directory_path.glob(file_pattern):
            try:
                file_chunks = chunk_file(str(file_path))
                chunks.extend(file_chunks)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
        
        return self.build_from_chunks(chunks)
    
    def compare(self, other: 'MerkleTree') -> List[str]:
        """
        Compare this Merkle tree with another tree and return a list of changed chunk IDs.
        
        Args:
            other: Another Merkle tree to compare with.
            
        Returns:
            List of chunk IDs (doc_ids) that have changed.
        """
        if not self.root or not other.root:
            return list(set(self.chunk_nodes.keys()) | set(other.chunk_nodes.keys()))
        
        changed_chunks = []
        
        # Compare root nodes
        if self.root.hash_value == other.root.hash_value:
            # Trees are identical
            return []
        
        # Compare file nodes
        self_file_nodes = {child.hash_value: child for child in self.root.children}
        other_file_nodes = {child.hash_value: child for child in other.root.children}
        
        # Find changed files
        changed_file_hashes = set(self_file_nodes.keys()) ^ set(other_file_nodes.keys())
        
        # Add all chunks from files that are in one tree but not the other
        for file_hash in changed_file_hashes:
            if file_hash in self_file_nodes:
                for chunk_node in self_file_nodes[file_hash].children:
                    changed_chunks.append(chunk_node.hash_value)
            elif file_hash in other_file_nodes:
                for chunk_node in other_file_nodes[file_hash].children:
                    changed_chunks.append(chunk_node.hash_value)
        
        # For files that exist in both trees, compare chunk by chunk
        common_file_hashes = set(self_file_nodes.keys()) & set(other_file_nodes.keys())
        for file_hash in common_file_hashes:
            self_file = self_file_nodes[file_hash]
            other_file = other_file_nodes[file_hash]
            
            if self_file.hash_value != other_file.hash_value:
                # File has changed, compare chunks
                self_chunks = {chunk.hash_value: chunk for chunk in self_file.children}
                other_chunks = {chunk.hash_value: chunk for chunk in other_file.children}
                
                # Find changed chunks
                changed_chunk_hashes = set(self_chunks.keys()) ^ set(other_chunks.keys())
                changed_chunks.extend(changed_chunk_hashes)
        
        return changed_chunks


def demo():
    """Demonstrate the Merkle tree with a simple example."""
    from pr_agent.algo.ast_chunker import chunk_code_string
    
    # Example code before changes
    code_before = """
def function_a():
    return "Hello World"

def function_b():
    return "Goodbye World"
    """
    
    # Example code after changes (function_b modified)
    code_after = """
def function_a():
    return "Hello World"

def function_b():
    return "Farewell World"
    """
    
    # Build Merkle tree from original code
    chunks_before = chunk_code_string(code_before, "example.py")
    tree_before = MerkleTree().build_from_chunks(chunks_before)
    
    # Build Merkle tree from modified code
    chunks_after = chunk_code_string(code_after, "example.py")
    tree_after = MerkleTree().build_from_chunks(chunks_after)
    
    # Compare trees to find changed chunks
    changed_chunk_ids = tree_before.compare(tree_after)
    
    print("Changed chunks:")
    for chunk_id in changed_chunk_ids:
        print(f"  - {chunk_id}")
    
    # Map chunk IDs back to chunks for more information
    print("\nDetails of changed chunks:")
    for chunk in chunks_after:
        if chunk.doc_id in changed_chunk_ids:
            print(f"  - {chunk.type} at lines {chunk.start_line}-{chunk.end_line}")
            print(f"    {chunk.code_string[:50]}...")


if __name__ == "__main__":
    demo() 