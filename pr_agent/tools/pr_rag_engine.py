from pr_agent.clients.kaito_rag_client import KAITORagClient
from pr_agent.git_providers import (get_git_provider,
                                    get_git_provider_with_context)
from pr_agent.algo.types import EDIT_TYPE

from ..log import get_logger
import base64


class PRRagEngine:
    def __init__(self, base_url: str):
        self.rag_client = KAITORagClient(base_url)
        # these are the languages that are supported by tree sitter
        self.valid_languages = ['bash', 'c', 'c_sharp','commonlisp', 'cpp', 'css', 'dockerfile', 'dot', 'elisp', 'elixir', 'elm', 'embedded_template', 'erlang', 'fixed_form_fortran', 'fortran', 'go', 'gomod', 'hack', 'haskell', 'hcl', 'html', 'java', 'javascript', 'jsdoc', 'json', 'julia', 'kotlin', 'lua', 'make', 'markdown', 'objc', 'ocaml', 'perl', 'php', 'python', 'ql', 'r', 'regex', 'rst', 'ruby', 'rust', 'scala', 'sql', 'sqlite', 'toml', 'tsq', 'typescript', 'yaml']

    def _get_git_provider(self, pr_url: str):
        git_provider = get_git_provider(pr_url)
        if not git_provider:
            get_logger().error(f"Git provider not found for PR URL {pr_url}.")
            raise ValueError("Git provider not found for the given PR URL.")
        return git_provider

    def _get_index_name(self, git_provider):
        if not git_provider:
            raise ValueError("Git provider not found for the given PR URL.")

        # Build index_name from repo and branch
        repo_name = git_provider.repo.replace('/', '_')
        branch_name = git_provider.get_pr_branch().replace('/', '_')
        index_name = f"{repo_name}_{branch_name}"
        return index_name
    
    def _get_default_branch_index_name(self, git_provider):
        if not git_provider:
            raise ValueError("Git provider not found for the given PR URL.")

        # Build index_name from repo and branch
        repo_name = git_provider.repo.replace('/', '_')
        branch_name = git_provider.repo_obj.default_branch.replace('/', '_')
        index_name = f"{repo_name}_{branch_name}"
        return index_name

    def _does_index_exist(self, index_name: str):
        try:
            resp = self.rag_client.list_indexes()
            if resp and index_name in resp:
                return True
        except Exception as e:
            get_logger().error(f"Error checking index existence: {e}")
            raise e
        return False
    
    def update_base_branch_index(self, pr_url: str):
        try:
            # Update the base branch index
            get_logger().info(f"Updating base branch index {pr_url}.")
            self.update_index(pr_url, for_base_branch=True)
        except Exception as e:
            get_logger().error(f"Error updating base branch index: {e}")
            raise e

    def create_base_branch_index(self, pr_url: str):
        git_provider = get_git_provider_with_context(pr_url)
        if not git_provider:
            get_logger().error(f"Git provider not found for PR URL {pr_url}.")
            raise ValueError("Git provider not found for the given PR URL.")

        index_name = self._get_default_branch_index_name(git_provider)
        print(f"Creating base branch index {index_name} for PR URL {pr_url}.")

        # Check if the index already exists
        if self._does_index_exist(index_name):
            get_logger().info(f"Index {index_name} already exists. Skipping creation.")
            return

        default_branch = git_provider.repo_obj.get_branch(git_provider.repo_obj.default_branch)
        if not default_branch:
            get_logger().error(f"Default branch {git_provider.repo_obj.default_branch} not found.")
            raise ValueError("Default branch not found for the given PR URL.")
        
        base_branch_tree = git_provider.repo_obj.get_git_tree(default_branch.commit.sha, recursive=True)
        batch_docs = []
        for file_info in base_branch_tree.tree:
            if file_info.type == "blob":
                # Might want to check file size / or other attributes here for filtering
                print(f"Indexing file {file_info.path} with sha {file_info.sha}")
                doc = {
                    "text": base64.b64decode(git_provider.repo_obj.get_git_blob(file_info.sha).content).decode(),
                    "metadata": {
                        "file_name": file_info.path,
                    }
                }
                print(f"Document created for file {file_info.path}: {doc}")
                batch_docs.append(doc)
                # no language info here yet
                # need to check file extensions go get it
            if len(batch_docs) >= 10:
                try:
                    self.rag_client.index_documents(index_name, batch_docs)
                except Exception as e:
                    get_logger().error(f"Error indexing documents: {e}")
                batch_docs = []
        if batch_docs:
            try:
                resp = self.rag_client.index_documents(index_name, batch_docs)
            except Exception as e:
                get_logger().error(f"Error indexing documents: {e}")
                raise e


    def create_new_pr_index(self, pr_url: str):
        git_provider = get_git_provider_with_context(pr_url)
        if not git_provider:
            get_logger().error(f"Git provider not found for PR URL {pr_url}.")
            raise ValueError("Git provider not found for the given PR URL.")

        index_name = self._get_index_name(git_provider)
        base_index_name = self._get_default_branch_index_name(git_provider)

        try:
            # Check if the base branch index already exists
            if not self._does_index_exist(base_index_name):
                self.create_base_branch_index(pr_url)

            # On create calls we will always overwrite the index in case of branch reusage
            get_logger().info(f"Creating new index {index_name} for PR URL {pr_url}.")
            self.rag_client.persist_index(base_index_name, path=f"/tmp/{base_index_name}")
            self.rag_client.load_index(index_name, path=f"/tmp/{base_index_name}", overwrite=True)
            
            self.update_index(pr_url)

        except Exception as e:
            get_logger().error(f"Error creating new pr index: {e}")
            raise e

    def update_index(self, pr_url: str, for_base_branch: bool = False):
        git_provider = get_git_provider_with_context(pr_url)
        if not git_provider:
            get_logger().error(f"Git provider not found for PR URL {pr_url}.")
            raise ValueError("Git provider not found for the given PR URL.")

        index_name = self._get_index_name(git_provider)
        base_index_name = self._get_default_branch_index_name(git_provider)

        try:
            diff_files = git_provider.get_diff_files()
            deleted_docs = []
            update_docs = []
            create_docs = []
            existing_docs = []
            for file_info in diff_files:
                resp = self.rag_client.list_documents(index_name, metadata_filter={"file_name": file_info.filename})
                if resp and resp.get("documents"):
                    existing_docs.extend(resp["documents"])

            for file_info in diff_files:
                doc = {
                    "text": file_info.head_file,
                    "metadata": {
                        "file_name": file_info.filename,
                    }
                }

                if file_info.language and file_info.language in self.valid_languages:
                    # will likely need to make a map of github languages to tree sitter languages
                    doc["metadata"]["language"] = file_info.language
                    doc["metadata"]["split_type"] = "code"
                
                curr_doc = None
                for existing_doc in existing_docs:
                    if file_info.filename == existing_doc["metadata"]["file_name"]:
                        curr_doc = existing_doc
                        break

                if file_info.edit_type == EDIT_TYPE.DELETED:
                    # Deleted files will be marked for deletion
                    deleted_docs.append(curr_doc)
                elif file_info.edit_type == EDIT_TYPE.MODIFIED or file_info.edit_type == EDIT_TYPE.RENAMED:
                    # Modified files will be updated
                    doc["text"] = git_provider.get_pr_file_content(file_info.filename, git_provider.get_pr_branch())
                    doc["metadata"]["file_name"] = file_info.filename
                    update_docs.append(doc)
                elif file_info.edit_type == EDIT_TYPE.ADDED:
                    # Added files will be created
                    doc = {
                        "text": git_provider.get_pr_file_content(file_info.filename, git_provider.get_pr_branch()),
                        "metadata": {
                            "file_name": file_info.filename,
                        }
                    }

                    if file_info.language and file_info.language in self.valid_languages:
                        # will likely need to make a map of github languages to tree sitter languages
                        doc["metadata"]["language"] = file_info.language
                        doc["metadata"]["split_type"] = "code"
                    
                    create_docs.append(doc)
                else:
                    # Unknown edit type, handle as needed
                    get_logger().warning(f"Unknown edit type for file {file_info.filename}: {file_info.edit_type}")
                    continue
            
            if not deleted_docs and not update_docs and not create_docs:
                get_logger().info(f"No changes detected for PR URL {pr_url}.")
                return

            if for_base_branch:
                print(f"Updating base branch index {base_index_name} for PR URL {pr_url}.")
                # If this is a base branch update, we need to delete the old index
                if deleted_docs:
                    print(f"Deleting documents from base index {base_index_name} for PR URL {pr_url}.")
                    resp = self.rag_client.delete_documents(base_index_name, [doc["doc_id"] for doc in deleted_docs])
                    print(f"Deleted documents: {resp}")
                if update_docs:
                    print(f"Updating documents in base index {base_index_name} for PR URL {pr_url}.")
                    resp = self.rag_client.update_documents(base_index_name, update_docs)
                    print(f"Updated documents: {resp}")
                if create_docs:
                    print(f"Creating documents in base index {base_index_name} for PR URL {pr_url}.")
                    resp = self.rag_client.index_documents(base_index_name, create_docs)
                    print(f"Created documents: {resp}")
            else:
                print(f"Updating index {index_name} for PR URL {pr_url}.")
                if deleted_docs:
                    print(f"Deleting documents from index {index_name} for PR URL {pr_url}.")
                    resp = self.rag_client.delete_documents(index_name, [doc["doc_id"] for doc in deleted_docs])
                    print(f"Deleted documents: {resp}")
                if update_docs:
                    print(f"Updating documents in index {index_name} for PR URL {pr_url}.")
                    resp = self.rag_client.update_documents(index_name, update_docs)
                    print(f"Updated documents: {resp}")
                if create_docs:
                    print(f"Creating documents in index {index_name} for PR URL {pr_url}.")
                    resp = self.rag_client.index_documents(index_name, create_docs)
                    print(f"Created documents: {resp}")
        except Exception as e:
            get_logger().error(f"Error updating documents: {e}")
            raise e

