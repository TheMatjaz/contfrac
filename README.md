ContFrac
===============================================================================

Continued fractions are a representation of numbers expressed as recursive
sums of integer parts and reciprocals of other numbers. _ContFrac_ is a
pure-Python3 lightweight module to compute and evaluate continued fractions,
as well as using them to approximate any number.  


Features
----------------------------------------

- Supports conversion into continued fractions of `int`, `float`,
  `fractions.Fraction` and rational numbers expressed as tuples of 2 integers
  `(numerator, denominator)`, generated iteratively.
- Computes the convergents of the same data types, generated iteratively.
- Computes the value of a finite continued fraction.
- Generates the arithmetical expression as string of a continued fraction.


Installation
----------------------------------------

```bash
pip install contfrac
```

or just include the `contfrac.py` file in your project (copy-paste).


Example usage
----------------------------------------

```python
>>> import contfrac
>>> value = 415/93  # Express as (415, 93) to avoid rounding continued frac.
>>> coefficients = list(contfrac.continued_fraction(value))
>>> print(coefficients)
[4, 2, 6, 7]

>>> expression = contfrac.arithmetical_expr(coefficients)
>>> print('Value: {:f} = {:s}'.format(value, expression))
Value: 4.462366 = 4 + 1/(2 + 1/(6 + 1/(7)))

>>> # The evaluation of a float value from a continued fraction is subject
>>> # to floating point rounding errors
>>> eval_value = contfrac.evaluate(coefficients)
>>> print(eval_value, value)  # Visible rounding errors
4.46236559139785 4.462365591397849

>>> convergents = list(contfrac.convergents(value))
>>> print(convergents)
[(4, 1), (9, 2), (58, 13), (415, 93)]

>>> import math
>>> coefficients = list(contfrac.continued_fraction(math.e, maxlen=10))
>>> print(coefficients)
[2, 1, 2, 1, 1, 4, 1, 1, 6, 1]

>>> convergent = contfrac.convergent(math.e, 3)  # Low convergent grade
>>> print(convergent, convergent[0]/convergent[1], math.e)
(11, 4) 2.75 2.718281828459045

>>> convergent = contfrac.convergent(math.e, 7)  # Higher grade = more accurate
>>> print(convergent, convergent[0]/convergent[1], math.e)
(193, 71) 2.7183098591549295 2.718281828459045
```


Similar libraries
----------------------------------------

- [Continued](https://github.com/MostAwesomeDude/continued), also available
  through `pip` 
