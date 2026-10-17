import os
import unittest
from unittest.mock import patch
from app.main import student_info, message


class StudentTests(unittest.TestCase):
    def test_default_identity(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(student_info(), {'Name': 'Vyacheslav', 'Surname': 'Kim',
                                             'Group': 'IT2-2312', 'Student ID': '37746'})

    def test_environment_overrides_all_fields(self):
        with patch.dict(os.environ, {'STUDENT_NAME': 'Test', 'STUDENT_SURNAME': 'User',
                                     'STUDENT_GROUP': 'TEST', 'STUDENT_ID': '42'}):
            self.assertEqual(student_info(), {'Name': 'Test', 'Surname': 'User',
                                             'Group': 'TEST', 'Student ID': '42'})
            self.assertIn('Student ID: 42', message())
            self.assertNotIn('37746', message())


if __name__ == '__main__':
    unittest.main()
