from util_module import RepositoryLoader
from settings import Settings
from git_miner import Project


class Main:

    def __init__(self):
        self.repositories = []
        self.settings = Settings()

    def _load_projects(self):
        projects = []

        repository_loader = RepositoryLoader(self.settings.get_repository_file_path())
        loaded_projects = repository_loader.load()

        for p in loaded_projects:
            project = Project(
                p['repo_name'],
                p["git_url"],
                p["branch"],
                p["starting_commit"],
                p["ending_commit"]
            )

            projects.append(project)

        return projects

    def start(self):
        projects = self._load_projects()

        for project in projects:
            project.collect_statistics()
            print(str(project.get_statistics()))

    def collect_smells_initial_commit(self):
        projects = self._load_projects()

        for p in projects:
            p.collect_statistics()
            # call method from project to detect smells
            p.detect_smells_initial_commit()


main = Main()
main.start()
main.collect_smells_initial_commit()
