import os
import git
import shutil
from settings import Settings


class RepositoryClone:

    @staticmethod
    def clone(repo_name, repo_url, repo_branch) -> str:
        settings = Settings()
        output_folder = settings.get_output_folder_path()
        src_folder = settings.get_source_folder()

        # ./miner-output/name_project/source
        repo_local_path = os.path.join(output_folder, repo_name, src_folder)

        # check if the folder exits, deleting if so
        if os.path.exists(repo_local_path):
            shutil.rmtree(repo_local_path)

        # it creates all the intermediate folders
        os.makedirs(repo_local_path)

        git.Repo.clone_from(repo_url, repo_local_path, branch=repo_branch)

        return repo_local_path
