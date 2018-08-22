import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split_important(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

# load all test methods from a TestCase class
common_suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)

# add only 1 test method
one_case_suite = unittest.TestSuite()
one_case_suite.addTest(TestStringMethods('test_upper'))

# only run test methods the name of which ends with important
only_run_important_suite = unittest.TestSuite()
for case in [method for method in dir(TestStringMethods) if method.endswith('important')]:
    only_run_important_suite.addTest(TestStringMethods(case))

# run test methods in custom order
custom_order_suite = unittest.TestSuite()
for case in sorted([method for method in dir(TestStringMethods) if method.startswith('test_')], key=len, reverse=True):
    custom_order_suite.addTest(TestStringMethods(case))


# unittest.TextTestRunner(verbosity=2).run(common_suite)
# unittest.TextTestRunner(verbosity=2).run(one_case_suite)
# unittest.TextTestRunner(verbosity=2).run(only_run_important_suite)
unittest.TextTestRunner(verbosity=2).run(custom_order_suite)
