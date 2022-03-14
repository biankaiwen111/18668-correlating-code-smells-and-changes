class ProjectSmells:




    def __init__(self):
        # array with all the smelly elements including classes and method
        self.smelly_elements = []

    def add_smelly_class(self, smelly_class):
        self.smelly_elements.append(smelly_class)

    def get_total_smells(self):
        total_class = 0
        total_method = 0

        for e in self.smelly_elements:
            total_class += len(e.get_class_smells())
            total_method += len(e.get_method_smells())

        return total_class, total_method

    def __str__(self):
        total_class, total_method = self.get_total_smells()
        return f'Commit has {len(self.smelly_elements)} smelly classes with a total of {total_class + total_method}' \
               f' smells: {total_class} class-level smells and {total_method} method-level smells'

    ## innner class to store the smells of the class
    class SmellyClass:

        def __init__(self, fully_qualified_name, path):
            self.fully_qualified_name = fully_qualified_name
            self.path = path
            self.class_smells = []
            self.method_smells = []

        def has_smells(self):
            # in python, an empty array is always false
            return self.class_smells or self.method_smells

        def add_class_level_smells(self, smell_list):
            if smell_list is not None:
                self.class_smells += smell_list

        def add_method_level_smells(self, method_list):
            if method_list is not None:
                self.method_smells += method_list

        def get_class_smells(self):
            return self.class_smells

        def get_method_smells(self):
            return self.method_smells
