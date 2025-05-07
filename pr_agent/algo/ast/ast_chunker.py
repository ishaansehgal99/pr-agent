"""
AST-based code chunking module for the PR Agent.

This module uses tree-sitter to parse Python code into an Abstract Syntax Tree (AST),
then extracts meaningful logical units (functions, classes, methods) to be used
as chunks for the Merkle tree and RagEngine indexing.
"""

import os
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging

# Tree-sitter imports
from tree_sitter import Language, Parser

logger = logging.getLogger(__name__)

@dataclass
class CodeChunk:
    """Represents a semantically meaningful chunk of code from a source file."""
    code_string: str
    type: str  # 'function', 'class', 'method', etc.
    start_line: int
    end_line: int
    path: str
    
    @property
    def doc_id(self) -> str:
        """Generate a document ID by hashing the normalized code content."""
        normalized = self.normalize_code(self.code_string)
        return f"{self.path}__{hashlib.sha256(normalized.encode()).hexdigest()}"
    
    @staticmethod
    def normalize_code(code: str) -> str:
        """Normalize code by removing whitespace variations."""
        # This is a basic implementation; more sophisticated normalization might be needed
        lines = [line.strip() for line in code.split('\n')]
        return '\n'.join(line for line in lines if line)


class TreeSitterSetup:
    """Manages tree-sitter setup and language loading."""
    
    def __init__(self, languages_dir: Optional[str] = None):
        """
        Initialize tree-sitter setup.
        
        Args:
            languages_dir: Directory where tree-sitter language libraries are stored.
                           If None, will use a default directory.
        """
        if languages_dir is None:
            # Default to a directory within the project
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            languages_dir = os.path.join(base_dir, 'tree-sitter-languages')
            
        self.languages_dir = languages_dir
        self._ensure_languages_dir()
        self.language = None
        self.parser = None
        
    def _ensure_languages_dir(self):
        """Ensure the languages directory exists."""
        os.makedirs(self.languages_dir, exist_ok=True)
        
    def build_language(self, force_rebuild: bool = False) -> Language:
        """
        Build or load the tree-sitter Python language.
        
        Args:
            force_rebuild: If True, rebuild the language even if it already exists.
            
        Returns:
            The tree-sitter Language object for Python.
        """
        language_file = os.path.join(self.languages_dir, 'python.so')
        
        if not os.path.exists(language_file) or force_rebuild:
            logger.info("Building tree-sitter Python language")
            # This requires tree-sitter-python repository
            # We should document the setup instructions or handle it automatically
            Language.build_library(
                language_file,
                [os.path.join(self.languages_dir, 'tree-sitter-python')]
            )
        
        self.language = Language(language_file, 'python')
        return self.language
    
    def get_parser(self) -> Parser:
        """
        Get a configured tree-sitter parser for Python.
        
        Returns:
            A configured Parser object.
        """
        if self.language is None:
            self.build_language()
            
        if self.parser is None:
            self.parser = Parser()
            self.parser.set_language(self.language)
            
        return self.parser


class ASTChunker:
    """Chunker that uses AST to extract semantic code units."""
    
    def __init__(self, parser: Optional[Parser] = None):
        """
        Initialize the AST chunker.
        
        Args:
            parser: A configured tree-sitter parser. If None, a new one will be created.
        """
        if parser is None:
            setup = TreeSitterSetup()
            self.parser = setup.get_parser()
        else:
            self.parser = parser
    
    def chunk_code(self, code: str, file_path: str) -> List[CodeChunk]:
        """
        Parse code string and extract semantic chunks.
        
        Args:
            code: String containing Python source code.
            file_path: Path to the source file (used for doc_id generation).
            
        Returns:
            List of CodeChunk objects representing semantic units in the code.
        """
        tree = self.parser.parse(bytes(code, 'utf8'))
        root_node = tree.root_node
        
        chunks = []
        
        # Process top-level nodes
        for child in root_node.children:
            if child.type == 'class_definition':
                chunks.extend(self._process_class(child, code, file_path))
            elif child.type == 'function_definition':
                chunks.append(self._extract_chunk(child, code, 'function', file_path))
        
        return chunks
    
    def _process_class(self, node: Any, code: str, file_path: str) -> List[CodeChunk]:
        """
        Process a class node, extracting the class itself and its methods.
        
        Args:
            node: tree-sitter AST node representing a class.
            code: Original source code string.
            file_path: Path to the source file.
            
        Returns:
            List of CodeChunk objects for the class and its methods.
        """
        chunks = [self._extract_chunk(node, code, 'class', file_path)]
        
        # Find the class body
        body_node = None
        for child in node.children:
            if child.type == 'block':
                body_node = child
                break
        
        if body_node:
            # Extract methods from the class body
            for child in body_node.children:
                if child.type == 'function_definition':
                    chunks.append(self._extract_chunk(child, code, 'method', file_path))
        
        return chunks
    
    def _extract_chunk(self, node: Any, code: str, chunk_type: str, file_path: str) -> CodeChunk:
        """
        Extract a code chunk from an AST node.
        
        Args:
            node: tree-sitter AST node.
            code: Original source code string.
            chunk_type: Type of the chunk ('function', 'class', 'method').
            file_path: Path to the source file.
            
        Returns:
            A CodeChunk object representing the extracted code.
        """
        start_byte = node.start_byte
        end_byte = node.end_byte
        
        # Extract the code string
        code_bytes = code.encode('utf8')
        chunk_bytes = code_bytes[start_byte:end_byte]
        chunk_str = chunk_bytes.decode('utf8')
        
        # Get line numbers
        start_line = node.start_point[0] + 1  # tree-sitter uses 0-based indexing
        end_line = node.end_point[0] + 1
        
        return CodeChunk(
            code_string=chunk_str,
            type=chunk_type,
            start_line=start_line,
            end_line=end_line,
            path=file_path
        )


def chunk_file(file_path: str) -> List[CodeChunk]:
    """
    Parse a Python file and extract semantic chunks.
    
    Args:
        file_path: Path to the Python file.
        
    Returns:
        List of CodeChunk objects.
    """
    chunker = ASTChunker()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    return chunker.chunk_code(code, os.path.abspath(file_path))


def chunk_code_string(code: str, file_path: str = "unknown.py") -> List[CodeChunk]:
    """
    Parse a Python code string and extract semantic chunks.
    
    Args:
        code: Python code as a string.
        file_path: A name/path to associate with this code for doc_id generation.
        
    Returns:
        List of CodeChunk objects.
    """
    chunker = ASTChunker()
    return chunker.chunk_code(code, file_path) 