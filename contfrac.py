#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing


def value_finite(cont_frac):
    """Computes the floating point value of a finite continued fraction
    representation.

    That is the value of `c[0] + 1/(c[1] + 1/(c[2] + 1/(c[3] + ...)))`
    for an input `c`.

    Args:
        cont_frac (Iterable[Union[int, float]]): representation of a continued
            fraction as iterable of numbers.

    Returns:
        float: the value of the continued fraction.
    """
    if isinstance(cont_frac, typing.Generator):
        cont_frac = list(cont_frac)
    if len(cont_frac) == 0:
        return 0
    fraction = 0
    for i, coefficient in enumerate(reversed(cont_frac[1:])):
        fraction = 1 / (coefficient + fraction)
    return cont_frac[0] + fraction


def arithmetical_expr(cont_frac, with_spaces=True, force_floats=False):
    """Generates the arithmetical expression as string of a continued fraction.

    The string is ready to be evaluated by a functions like `eval()` or
    by other programming languages or calculators. Beware of integer division
    instead of true division in said language: use the `force_floats` argument.

    Args:
        cont_frac (Iterable[Union[int, float]]): representation of a continued
            fraction as iterable of numbers.
        with_spaces (bool): places a whitespace around the plus sign when True.
            Used to increase readability of the expression.
        force_floats (bool): forces the fraction expression to be `1.0/x`
            instead of `1/x` to avoid integer division when evaluating the
            string in some programming languages.

    Returns:
        str: the arithmetical expression to evaluate the continued fraction's
             value.
    """
    parts = []
    i = 0
    for i, coefficient in enumerate(cont_frac):
        parts.append(str(coefficient))
    if with_spaces:
        joiner = ' + '
    else:
        joiner = '+'
    if force_floats:
        joiner += '1.0/('
    else:
        joiner += '1/('
    return joiner.join(parts) + ')' * i
