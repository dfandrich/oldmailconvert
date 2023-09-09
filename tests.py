"""Run all the unit tests."""

import unittest


def tests():
    return unittest.TestLoader().discover('.', pattern='*_test.py')


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(tests())
