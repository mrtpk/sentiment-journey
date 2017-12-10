import unittest
from n_grams import clean 

class TestHelperMethods(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(clean('''&"'`~@#$%^*;+=<>//.,()[]{}:;'''),"")

if __name__ == '__main__':
    unittest.main()