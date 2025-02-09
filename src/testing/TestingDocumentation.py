from datetime import datetime

from lib.AutoTestingDocumentation.src.testing.TestingFunction import TestingFunction


class TestingDocumentation:

    def __init__(self, index: int, name: str = "", description: str = ""):
        self.index  = index
        self.name = name
        self.description = description
        self.test_list: list[TestingFunction] = []

    def add_test(self, test_function: TestingFunction):
        self.test_list.append(test_function)

    def to_csv(self):

        fieldnames = [f"col{i+1}" for i in range(6)]
        rows = [
            {"col2": "Titre de l'essai", "col4": "ID de l'essai", "col6": "Date de l'essai"},
            {"col2": self.name, "col4": self.index, "col6": datetime.now().strftime("%d/%m/%Y %H:%M:%S")},
            {"col2": "Description de l'essai", "col4": "Nom du testeur"},
            {"col2": self.description, "col3": "Louis Dubois"},
            {"col1": "N°", "col2": "ACTION", "col3": "VALEUR D'ENTREE", "col4": "ATTENDU", "col5": "RESULTAT", "col6": "MODIFICATION"},
        ]
        for test in self.test_list:
            rows.append(test.to_csv())
        return fieldnames, rows

    def __str__(self):
        returned_string = ""
        for key in self.__dict__.keys():
            returned_string += f"{key.title()}: {getattr(self, key)}\n"
        return returned_string