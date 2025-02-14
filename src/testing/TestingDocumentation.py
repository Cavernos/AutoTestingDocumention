import unittest
from datetime import datetime
from typing import Type
from unittest import TestCase, TestResult

from auto_testing_documentation.testing import TestingFunction


class TestingDocumentation:
    """
    This class is used to generate a Test sheet for all test function in unittest TestCase class
    """

    def __init__(self, index: int, testing_class: Type[TestCase], name: str = "", description: str = ""):
        self.index  = index
        self.name = testing_class.__name__ if hasattr(testing_class, "__name__") else name
        self.description = description
        self.testing_class = testing_class
        self.test_list: list[TestingFunction] = []

    def add_test(self, test_function: TestingFunction):
        self.test_list.append(test_function)

    def add_test_from_class(self) -> None:
        """
        This function add test to test list from pasted_class
        :return: None
        """
        if hasattr(self.testing_class, "test_documentation"):
            test_list = None
            for name, function in self.testing_class.__dict__.items():
                    if name in self.testing_class.test_documentation.keys():
                        for i, value in enumerate(self.testing_class.test_documentation[name].values()):
                            if isinstance(value, list):
                                if i == 0:
                                    test_list = [TestingFunction() for i in range(len(value))]
                                for index, item in enumerate(value):
                                    if isinstance(item, tuple):
                                        test_list[index].index=item[0] -2
                                        test_list[index].name = f'{name}_{len(item[1])}_digits'
                                        test_list[index].expected = item[2]
                                        test_list[index].enter_value = ''.join(item[1])
                                    else:
                                        test_list[index].real_return_value = item
                        self.test_list = test_list if test_list is not None else []

    def to_csv(self) -> tuple:
        """
        This function convert all information in csv format to make excel sheet

        :return: tuple, Return a tuple to format information in csv
        """
        fieldnames = [f"col{i+1}" for i in range(7)]
        rows = [
            {"col2": "Titre de l'essai", "col4": "ID de l'essai", "col6": "Date de l'essai"},
            {"col2": self.name, "col4": self.index, "col6": datetime.now().strftime("%d/%m/%Y %H:%M:%S")},
            {"col2": "Description de l'essai", "col4": "Nom du testeur"},
            {"col2": self.description, "col4": "Louis Dubois"},
            {"col1": "N°", "col2": "ACTION", "col3": "VALEUR D'ENTREE", "col4": "RESULTAT", "col5": "ATTENDU", "col6": "STATUS", "col7": "MODIFICATION"},
        ]
        for test in self.test_list:
            rows.append(test.to_csv())
        return fieldnames, rows

    def run(self)-> TestResult:
        """
        This function runs all tests and return the tests results

        :return: TestResult, TestResult object which contain all test information
        """
        runner = unittest.TextTestRunner(verbosity=0, descriptions=False)
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(self.testing_class)
        test_result = runner.run(suite)
        self.add_test_from_class()
        for index, function in enumerate(self.test_list):

            if len(test_result.errors) != 0:
                for test in test_result.errors:
                    if test[0]._testMethodName == function.name:
                        function.status = "ERROR"
                        break
                    else:
                        function.status = "PASSED"
            elif len(test_result.skipped) != 0:
                for test in test_result.skipped:
                    if test[0]._testMethodName == function.name:
                        function.status = "SKIPPED"
                        break
                    else:
                        function.status = "PASSED"
            elif len(test_result.failures) != 0:
                for test in test_result.failures:
                    if test[0]._testMethodName == function.name:
                        function.status = "FAILED"
                        break
                    else:
                        function.status = "PASSED"
        return test_result

    def __str__(self):
        returned_string = ""
        for key in self.__dict__.keys():
            returned_string += f"{key.title()}: {getattr(self, key)}\n"
        return returned_string

# if __name__ == "__main__":
#     from tests.kaprekar.test_kaprekar import TestKaprekar
#     documentation = TestingDocumentation(0, TestKaprekar, description=inspect.getdoc(TestKaprekar).splitlines()[0])
#     documentation.run()
#     with open("test.csv", 'w', newline='') as csvfile:
#         fieldnames, rows = documentation.to_csv()
#         csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames, dialect='excel').writerows(rows)
#     print(documentation)