from pydriller import Repository
from util_module import RepositoryClone
from pydriller import Git
from smell_detector import Organic, OrganicParser


class Project:

    def __init__(self, name, url, branch, starting_commit, ending_commit):
        self.name = name
        self.branch = branch
        self.url = url
        self.starting_commit = starting_commit
        self.ending_commit = ending_commit
        self.commit_hashes = []

        self.git = None

        #  {author_name: n of modified files}
        self.author_modified_files = {}
        self.commit_most_modified_lines = {'hash': None, 'lines': 0}
        self.modified_files = {}

    def collect_statistics(self):
        repo = Repository(self.url, from_commit=self.starting_commit, to_commit=self.ending_commit)

        generator = repo.traverse_commits()
        counter = 1
        for commit in generator:
            if counter == 1:
                print(commit.parents)
            counter += 1
            self.process_commit(commit)

    def process_commit(self, commit):
        modified_file = []
        if_discard = True
        for file in commit.modified_files:
            if file.filename.endswith(".java"):
                if_discard = False
            modified_file.append(file.filename)
        if if_discard:
            return
        self.commit_hashes.append(commit.hash)
        self.modified_files[commit.hash] = modified_file

        ##print(modified_file, commit.hash)

        author_name = commit.author.name
        modified_files = commit.files

        if author_name in self.author_modified_files:
            self.author_modified_files[author_name] += modified_files
        else:
            self.author_modified_files[author_name] = modified_files

        modified_lines = commit.lines
        if self.commit_most_modified_lines['lines'] < modified_lines:
            self.commit_most_modified_lines = {'hash': commit.hash, 'lines': modified_lines}

    def get_statistics(self):
        _hash, _lines = self.commit_most_modified_lines.values()

        author_name = max(self.author_modified_files, key=self.author_modified_files.get)

        return f'Project name: {self.name}:\n ' \
               f'\tThe author with most modifications is {author_name} with ' \
               f'{self.author_modified_files[author_name]} modified files.\n' \
               f'\tThe commit with most modifie lines is {_hash} with {_lines} modified lines.'

    def detect_smells_initial_commit(self):
        repo_local_path = RepositoryClone.clone(self.name, self.url, self.branch)
        print(self.commit_hashes)
        previous_project_smells = None
        with open("./result.txt", "w") as file:
            for hash in self.commit_hashes:
                print(hash, " : ")
                # we want to checkout the project to initial commit
                self.git = Git(repo_local_path)
                self.git.checkout(hash)

                # detect the code smells
                organic = Organic(self.name, repo_local_path)
                smell_file_path = organic.detect_smells()

                # parse the file
                parser = OrganicParser(smell_file_path)

                project_smells = parser.parse()

                unchanged_classes_smells, changed_classes_smells = \
                    self.compare_two_commit_smells(previous_project_smells, self.git.get_commit(hash))
                file.write(f"{unchanged_classes_smells} {changed_classes_smells} \n")
                previous_project_smells = project_smells

                # do comparison with previous commit
                print(project_smells.smelly_elements)
                print(project_smells)

    def compare_two_commit_smells(self, previous_smells, commit):
        prefix = "miner-output/junit4/source/"
        if not previous_smells:
            return None, None
        total_num_of_smells = sum(previous_smells.get_total_smells())
        changed_classes_smells = 0
        modified_files = commit.modified_files
        for file in modified_files:
            print(file.change_type.name)
            if file.change_type.name == "ADD":
                continue
            elif file.change_type.name == "MODIFY" or file.change_type.name == "DELETE":
                file_name = file.filename
                old_path = file.old_path
                if not file_name.endswith(".java"):
                    continue
                print(old_path, file_name)
                if '/test' in old_path:
                    continue
                for class_smell in previous_smells.smelly_elements:
                    if prefix + old_path == class_smell.path:
                        changed_classes_smells += len(class_smell.get_class_smells())
                        changed_classes_smells += len(class_smell.get_method_smells())
            else:
                continue
        unchanged_classes_smells = total_num_of_smells - changed_classes_smells
        print(unchanged_classes_smells, changed_classes_smells)
        return unchanged_classes_smells, changed_classes_smells




