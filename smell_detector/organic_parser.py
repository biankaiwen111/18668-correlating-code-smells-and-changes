import json
from .organic_smells import ProjectSmells


def _get_smells(data):
    smells = []

    if not data:
        return None

    for d in data:
        smells.append(d['name'])

    return smells


class OrganicParser:

    def __init__(self, smell_file_path):
        self.smell_file = smell_file_path

    def parse(self) -> ProjectSmells:
        with open(self.smell_file) as smell_file:
            data = json.load(smell_file)

        project_smells = ProjectSmells()

        # parse all smells, starting with the class level smells
        for d in data:
            # filter out the test class
            if '/test' in d['sourceFile']['fileRelativePath']:
                continue

            smelly_class = project_smells.SmellyClass(d['fullyQualifiedName'], d['sourceFile']['fileRelativePath'])
            smelly_class.add_class_level_smells(_get_smells(d['smells']))

            # get the smells from every method in the class
            for method in d['methods']:
                if method['smells']:
                    smelly_class.add_method_level_smells(_get_smells(method['smells']))

            if smelly_class.has_smells():
                project_smells.add_smelly_class(smelly_class)

        return project_smells

