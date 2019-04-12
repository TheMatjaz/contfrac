#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fractions
import math
import unittest

import contfrac


class TestEvaluateContfrac(unittest.TestCase):
    def test_evaluate_continued_fraction(self):
        test_values = {
            (): 0,
            (0,): 0,
            (1,): 1,
            (20,): 20,
            (0, 20): 1 / 20,
            (-20,): -20,
            (1, 2): 1 + 1 / 2,
            (-1, 2): -1 + 1 / 2,
            (0, 1): 0 + 1 / 1,
            (0, 0, 0, 1): 0 + 1 / (0 + (1 / (0 + (1 / 1)))),
            (0, 0, 0, 17): 0 + 1 / (0 + (1 / (0 + (1 / 17)))),
            (1, 2, 3): 1 + 1 / (2 + 1 / 3),
            (1, 2, 3, 4): 1 + 1 / (2 + (1 / (3 + (1 / 4)))),
            (1, 2, -3, 4): 1 + 1 / (2 + (1 / (-3 + (1 / 4)))),
            (1.1, 2, -3.34, 4): 1.1 + 1 / (2 + (1 / (-3.34 + (1 / 4)))),
            (3, 4, 12, 4): 649 / 200,
            (4, 2, 6, 7): 415 / 93,
            range(1, 5): 1 + 1 / (2 + (1 / (3 + (1 / 4)))),
            b'CD': 67 + 1 / 68,
        }
        for input_value, expected_output in test_values.items():
            with self.subTest(contfrac_of=input_value):
                result = contfrac.evaluate(input_value)
                self.assertAlmostEqual(expected_output, result, places=6)

    def test_evaluate_continued_fraction_with_zero_end(self):
        values = [
            [1, 0],
            [1, 2, 3, 0],
            [1, 2, 3, 0.0],
            [1, 2, 3, 0, 0, 0, 0],
        ]
        for value in values:
            with self.subTest(input_value=value):
                with self.assertRaises(ZeroDivisionError):
                    contfrac.evaluate(value)

    def test_evaluate_continued_fraction_unsupported_type_raises(self):
        self.assertRaises(TypeError, contfrac.evaluate, None)
        self.assertRaises(TypeError, contfrac.evaluate, 1)
        self.assertRaises(TypeError, contfrac.evaluate, 1.1)
        self.assertRaises(TypeError, contfrac.evaluate, 'hello')


class TestArithmeticExpression(unittest.TestCase):
    def test_expression_continued_fraction(self):
        test_values = {
            (): '',
            (0,): '0',
            (1,): '1',
            (20,): '20',
            (0, 20): '0 + 1/(20)',
            (-20,): '-20',
            (1, 2): '1 + 1/(2)',
            (-1, 2): '-1 + 1/(2)',
            (1, -2): '1 + 1/(-2)',
            (0, 1): '0 + 1/(1)',
            (0, 0, 0, 1): '0 + 1/(0 + 1/(0 + 1/(1)))',
            (0, 0, 0, 17): '0 + 1/(0 + 1/(0 + 1/(17)))',
            (1, 2, 3): '1 + 1/(2 + 1/(3))',
            (1, 2, 3, 4): '1 + 1/(2 + 1/(3 + 1/(4)))',
            (1, 2, -3, 4): '1 + 1/(2 + 1/(-3 + 1/(4)))',
            (1.1, 2, -3.34, 4): '1.1 + 1/(2 + 1/(-3.34 + 1/(4)))',
            range(1, 5): '1 + 1/(2 + 1/(3 + 1/(4)))',
        }
        for input_value, expected_default in test_values.items():
            with self.subTest(contfrac_of=input_value):
                result = contfrac.arithmetical_expr(input_value)
                expected_output = expected_default
                self.assertEqual(expected_output, result)
            with self.subTest(contfrac_of=input_value, spaces=False):
                result = contfrac.arithmetical_expr(input_value,
                                                    with_spaces=False)
                expected_output = expected_default.replace(' ', '')
                self.assertEqual(expected_output, result)
            with self.subTest(contfrac_of=input_value, floats=True):
                result = contfrac.arithmetical_expr(input_value,
                                                    force_floats=True)
                expected_output = expected_default.replace('1/', '1.0/')
                self.assertEqual(expected_output, result)
            with self.subTest(contfrac_of=input_value,
                              spaces=False, floats=True):
                result = contfrac.arithmetical_expr(input_value,
                                                    with_spaces=False,
                                                    force_floats=True)
                expected_output = expected_default.replace(' ', '')
                expected_output = expected_output.replace('1/', '1.0/')
                self.assertEqual(expected_output, result)


class TestContfracComputation(unittest.TestCase):
    def test_continued_fraction_legal_values(self):
        test_values = {
            # Integers
            0: [0],
            1: [1],
            123: [123],
            -1: [-1],
            -123: [-123],

            # Tuples: (nominator, denominator)
            (649, 200): [3, 4, 12, 4],
            (415, 93): [4, 2, 6, 7],
            (-649, 200): [-4, 1, 3, 12, 4],
            (415, -93): [-5, 1, 1, 6, 7],

            # Fractions
            fractions.Fraction(649, 200): [3, 4, 12, 4],
            fractions.Fraction(415, 93): [4, 2, 6, 7],
            fractions.Fraction(-649, 200): [-4, 1, 3, 12, 4],
            fractions.Fraction(415, -93): [-5, 1, 1, 6, 7],

            # Floats
            649 / 200: [3, 4, 12, 4],
            -649 / 200: [-3, -4, -12, -4],
            415 / 93: [4, 2, 6, 7],
            0.84375: [0, 1, 5, 2, 2],
        }
        for input_value, expected_output in test_values.items():
            with self.subTest(contfrac_of=input_value):
                result = contfrac.continued_fraction(input_value)
                self.assertListEqual(expected_output, result)
                with self.subTest(evaluating_contfrac_of=input_value):
                    if isinstance(input_value, tuple):
                        input_value = input_value[0] / input_value[1]
                    elif isinstance(input_value, fractions.Fraction):
                        input_value = float(input_value)
                    evaluated = contfrac.evaluate(result)
                    self.assertAlmostEqual(input_value, evaluated, delta=1e-8)

    def test_continued_fraction_illegal_maxlen(self):
        self.assertRaises(ValueError, contfrac.continued_fraction, 2.2,
                          maxlen=-1)
        self.assertRaises(ValueError, contfrac.continued_fraction, 2.2,
                          maxlen=0)
        contfrac.continued_fraction(2.2, maxlen=1)

    def test_continued_fraction_unsupported_type_raises(self):
        self.assertRaises(TypeError, contfrac.continued_fraction, None)
        self.assertRaises(TypeError, contfrac.continued_fraction, 'hello')
        self.assertRaises(TypeError, contfrac.continued_fraction, b'hello')
        self.assertRaises(TypeError, contfrac.continued_fraction, dict())

    def test_continued_fraction_golden_ratio(self):
        golden_ratio = (1 + math.sqrt(5)) / 2
        expected = [1] * 40
        result = contfrac.continued_fraction(golden_ratio, maxlen=2)
        self.assertListEqual(expected[:2], result)
        result = contfrac.continued_fraction(golden_ratio, maxlen=20)
        self.assertListEqual(expected[:20], result)
        result = contfrac.continued_fraction(golden_ratio, maxlen=31)
        self.assertListEqual(expected[:31], result)

    def test_rounding_errors(self):
        golden_ratio = (1 + math.sqrt(5)) / 2
        as_ratio = golden_ratio.as_integer_ratio()
        result = contfrac.continued_fraction(golden_ratio, maxlen=50)
        self.assertNotEqual([1] * 50, result)
        evaluated_value = contfrac.evaluate(result)
        self.assertEqual(golden_ratio, evaluated_value)
        result = contfrac.continued_fraction(as_ratio, maxlen=50)
        self.assertNotEqual([1] * 50, result)
        evaluated_value = contfrac.evaluate(result)
        self.assertEqual(as_ratio, evaluated_value.as_integer_ratio())
