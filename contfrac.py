#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fractions
import typing


def continued_fraction(x, maxlen=30):
    """Computes the continued fraction of a number ``x`` expressed in many
    types, including floats, tuples and Fractions.

    The result for a number ``x`` will be the list of coefficients
    ``[a, b, c, d, ...]```:

                           1
            x = a + ---------------
                             1
                    b + -----------
                               1
                        c + -------
                            d + ...


    Warning:
        If ``x`` is a float, then rounding errors may occur and the continued
        fraction is not guaranteed to look exactly as computed by hand,
        although if its value is evaluated with ``evaluate()``, it may be
        close-enough to ``x``.

        To avoid such issues, consider providing ``x`` as a ratio of integers,
        either as a tuple (numerator, denominator), which can be obtained from
        a float with its method ``as_integer_ratio()``, or as Fraction.
        Be aware that in this case the continued fraction may look
        different than computed by hand but its value once evaluated will
        be exactly the same as the input ratio.

        Given the finite precision a floating point value has, even an
        irrational number such as pi or e will be correctly represented
        up to a certain point in the continued fraction. For example the golden
        ratio will contain a ``2`` at index 38 of the continued fraction,
        when it should be ``1``.

    Args:
        x (Union[Tuple[int,int], float, int, fractions.Fraction]): the value
            to compute the continued fraction of.
        maxlen (int): upper limit to the length of the produced list,
            especially useful when computing continued fractions of irrational
            numbers.

    Returns:
        List[int]: continued fraction
    """
    if maxlen <= 0:
        raise ValueError('maxlen must be positive.')
    elif isinstance(x, int):
        return list(__int_cont_frac(x, 1, max_amount=1))
    elif isinstance(x, float):
        return list(__float_cont_frac(x, maxlen))
    elif isinstance(x, fractions.Fraction):
        return list(__int_cont_frac(x.numerator, x.denominator, maxlen))
    elif isinstance(x, (tuple, list)):
        return list(__int_cont_frac(x[0], x[1], maxlen))
    else:
        raise TypeError('Unsupported input type {:}'.format(type(x)))


def __int_cont_frac(num, den, max_amount):
    amount = 0
    while den != 0 and amount < max_amount:
        integer_part = num // den
        num -= integer_part * den
        num, den = den, num
        amount += 1
        yield integer_part


def __float_cont_frac(real_number, max_amount):
    fractional_part = 42
    amount = 0
    abs_tol = 10**-10
    while not abs(fractional_part) <= abs_tol and amount < max_amount:
        integer_part = int(round(real_number, 10))
        fractional_part = real_number - integer_part
        real_number = 1.0 / fractional_part
        amount += 1
        yield integer_part


def evaluate(cont_frac):
    """Computes the floating point value of a finite continued fraction
    representation.

    That is the value of ``c[0] + 1/(c[1] + 1/(c[2] + 1/(c[3] + ...)))``
    for an input ``c``.

    Example:
        For an input of ``[2,3,4]`` is ``2 + 1/(3 + 1/4) = 30/13`` expressed as
        2.3076923076923075.

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

    Example:
        It looks like ``2 + 1/(3 + 1/(4 + 1/(5)))`` for an input ``[2,3,4,5]``.

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
