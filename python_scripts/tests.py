from index import upload_repos
from check_file import check_file
from database import Database

import unittest

class TestSum(unittest.TestCase):
    def setUp(self):
        #here I used my own quite small old project repo
        self.db = Database()
        self.db.connect_database()


    def test_no_plagiarism(self):
        self.assertEqual(check_file('python_scripts/tests_content/no_plagiarism.java', self.db),
               'no plagiarism')

    def test_plagiarism(self):
        self.assertEqual(check_file('python_scripts/tests_content/plagiarism.java', self.db),
              'file repos/AMISquestions/app/src/main/java/ru/fmcs/hse/amisquestions/CreateNewPost.java seems to have plagiarism. The percentage is 88.73%')

    def test_total_plagiarism(self):
        self.assertEqual(check_file('python_scripts/tests_content/total_plagiarism.java', self.db),
              'file repos/AMISquestions/app/src/main/java/ru/fmcs/hse/amisquestions/CreateNewPost.java seems to have plagiarism. The percentage is 99.57%')

if __name__ == '__main__':
    #here I used small repo of my old project
    upload_repos(['https://github.com/polupanovaanna/AMISquestions'], '')
    unittest.main()