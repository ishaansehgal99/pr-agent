#!/usr/bin/env python
"""
Setup script for tree-sitter.

This script installs tree-sitter and the Python grammar needed for AST parsing.
"""

import os
import subprocess
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, cwd=None):
    """Run a shell command and log the output."""
    logger.info(f"Running command: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
        text=True, cwd=cwd
    )
    stdout, stderr = process.communicate()
    
    if stdout:
        logger.info(f"Command output: {stdout}")
    if stderr:
        logger.error(f"Command error: {stderr}")
        
    if process.returncode != 0:
        logger.error(f"Command failed with return code: {process.returncode}")
        return False
    return True

def install_tree_sitter():
    """Install the tree-sitter Python package."""
    logger.info("Installing tree-sitter package...")
    return run_command([sys.executable, "-m", "pip", "install", "tree-sitter"])

def setup_language_dir():
    """Create and return the path to the tree-sitter languages directory."""
    # Determine the base directory (project root)
    base_dir = Path(__file__).parent.parent.parent  # algo -> pr_agent -> project_root
    languages_dir = base_dir / "tree-sitter-languages"
    languages_dir.mkdir(exist_ok=True)
    return languages_dir

def clone_language_repo(languages_dir):
    """Clone the tree-sitter-python repository."""
    repo_path = languages_dir / "tree-sitter-python"
    
    if repo_path.exists():
        logger.info(f"Repository already exists at {repo_path}, updating...")
        return run_command(["git", "pull"], cwd=repo_path)
    
    logger.info(f"Cloning tree-sitter-python repository to {repo_path}...")
    return run_command([
        "git", "clone", "https://github.com/tree-sitter/tree-sitter-python.git", 
        str(repo_path)
    ])

def build_language(languages_dir):
    """Build the Python language library."""
    try:
        from tree_sitter import Language
        
        output_path = languages_dir / "python.so"
        repo_path = languages_dir / "tree-sitter-python"
        
        if output_path.exists():
            logger.info(f"Language library already exists at {output_path}")
            return True
        
        logger.info(f"Building Python language library to {output_path}...")
        Language.build_library(
            str(output_path),
            [str(repo_path)]
        )
        return True
    except Exception as e:
        logger.error(f"Error building language library: {e}")
        return False

def main():
    """Main function to set up tree-sitter."""
    logger.info("Setting up tree-sitter and Python grammar...")
    
    if not install_tree_sitter():
        logger.error("Failed to install tree-sitter")
        return False
    
    languages_dir = setup_language_dir()
    
    if not clone_language_repo(languages_dir):
        logger.error("Failed to clone language repository")
        return False
    
    if not build_language(languages_dir):
        logger.error("Failed to build language library")
        return False
    
    logger.info("Tree-sitter setup complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 