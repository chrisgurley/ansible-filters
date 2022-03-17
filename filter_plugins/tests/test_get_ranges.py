#!/usr/bin/python

import unittest
import random
import string

from get_ranges import FilterModule


class TestFilterModule(unittest.TestCase):

    def test_get_ranges_clean_sequential(self):

        module = FilterModule()
        testdata = [i for i in range(1,11)]
        self.assertEqual(len(module.get_ranges(testdata)), 1)
        self.assertEqual(module.get_ranges(testdata), ['1-10'])

    def test_get_ranges_clean_non_sequential(self):

        module = FilterModule()
        testdata = [i for i in range(1,11) if not i%2] + [i for i in range(1,11) if i%2]
        self.assertEqual(len(module.get_ranges(testdata)), 1)
        self.assertEqual(module.get_ranges(testdata), ['1-10'])

    def test_get_ranges_clean_non_sequential_duplicates(self):

        module = FilterModule()
        testdata = [i for i in range(1,11)] * 2
        random.shuffle(testdata)
        self.assertEqual(len(module.get_ranges(testdata)), 1)
        self.assertEqual(module.get_ranges(testdata), ['1-10'])

    def test_get_ranges_dirty_sequential(self):

        module = FilterModule()
        testdata = [i for i in range(1,11)] + [random.choice(string.ascii_lowercase) for i in range(100)]
        self.assertEqual(len(module.get_ranges(testdata)), 1)
        self.assertEqual(module.get_ranges(testdata), ['1-10'])

    def test_get_ranges_dirty_non_sequential(self):

        module = FilterModule()
        testdata = [i for i in range(1,11) if not i%2] + [i for i in range(1,11) if i%2] + [random.choice(string.ascii_lowercase) for i in range(100)]
        self.assertEqual(len(module.get_ranges(testdata)), 1)
        self.assertEqual(module.get_ranges(testdata), ['1-10'])

    def test_get_ranges_dirty_non_sequential_duplicates(self):

        module = FilterModule()
        testdata = [i for i in range(1,11)] * 2 + [random.choice(string.ascii_lowercase) for i in range(100)]
        random.shuffle(testdata)
        self.assertEqual(len(module.get_ranges(testdata)), 1)
        self.assertEqual(module.get_ranges(testdata), ['1-10'])

    def test_get_ranges_baddata_validate_type(self):

        module = FilterModule()
        testdata = [int, str, float, tuple, dict]
        for test in testdata:
            with self.assertRaises(TypeError):
                module.get_ranges(test)

    def test_get_ranges_baddata_validate_empty(self):

        module = FilterModule()
        testdata = []
        with self.assertRaises(ValueError):
            module.get_ranges(testdata)

    def test_get_ranges_baddata_safe(self):

        module = FilterModule()
        testdata = [[float], [str], [tuple], [dict]]
        for test in testdata:
            with self.assertRaises(ValueError):
                module.get_ranges(data=test, safe=True)

if __name__ == '__main__':
    unittest.main(verbosity=2)
