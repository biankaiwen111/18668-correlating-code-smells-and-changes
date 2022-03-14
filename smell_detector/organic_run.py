import os
import shutil
from settings import Settings
from util_module import bash
from util_module import verbose_decorator


class Organic:

    def __init__(self, repo_name, source_path):
        settings = Settings()
        output_folder = settings.get_output_folder_path()
        smell_folder = settings.get_smell_folder()
        smell_file = settings.get_smell_file()

        self.repo_name = repo_name
        self.detector = settings.get_smell_detector_path()
        self.output_folder = os.path.join(output_folder, repo_name, smell_folder)
        self.output_file_path = os.path.join(self.output_folder, smell_file)
        self.source = source_path

        # f-string
        self.command = f'java -jar "{self.detector}" -sf "{self.output_file_path}" -src "{self.source}"'

    def detect_smells(self):
        # check if folders exists, deleting if so
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)

        # we can recreate the intermediate folders
        os.makedirs(self.output_folder)

        # run organic
        run_command = verbose_decorator(bash.run_command, ":::DETECTING SMELLS:::")
        run_command(self.command, False)

        return self.output_file_path
