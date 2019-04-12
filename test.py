#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
                result = contfrac.value_finite(input_value)
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
                    contfrac.value_finite(value)

    def test_evaluate_continued_fraction_unsupported_type_raises(self):
        self.assertRaises(TypeError, contfrac.value_finite, None)
        self.assertRaises(TypeError, contfrac.value_finite, 1)
        self.assertRaises(TypeError, contfrac.value_finite, 1.1)
        self.assertRaises(TypeError, contfrac.value_finite, 'hello')


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
