import unittest

from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    heading = "Result for {} directory:\n"
    def test_calculator(self):
        expected = """ - main.py: file_size=718 bytes, is_dir=False
 - tests.py: file_size=1330 bytes, is_dir=False
 - pkg: file_size=4096 bytes, is_dir=True"""

        result = get_files_info("calculator", ".")
        print(self.heading.format("current"), result, "\n")
        self.assertEqual(result, expected)

    def test_calculator_pkg(self):
        expected = """ - render.py: file_size=375 bytes, is_dir=False
 - calculator.py: file_size=1720 bytes, is_dir=False"""

        result = get_files_info("calculator", "pkg")
        print(self.heading.format("'pkg'"), result, "\n")
        self.assertEqual(result, expected)

    def test_calculator_slash_bin(self):
        expected = 'Error: Cannot list "/bin" as it is outside the permitted working directory'

        result = get_files_info("calculator", "/bin")
        print(self.heading.format("'/bin'"), result, "\n")
        self.assertEqual(result, expected)

    def test_calculator_parent(self):
        expected = 'Error: Cannot list "../" as it is outside the permitted working directory'

        result = get_files_info("calculator", "../")
        print(self.heading.format("'../'"), result, "\n")
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()