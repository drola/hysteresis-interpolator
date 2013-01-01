Hysteresis interpolator
=======================
This is a simple class based on NumPy/SciPy that enables you to interpolate
values of a function with respect to direction. You get one curve when ascending
and the other one when declining.

Usage
-----

If you have a datafile with columns like this:

	#H [A/m]	B[T]
	...rows with values over time...

you can obtain value of B at any H like this:
```python
from HysteresisInterpolator import *
ip = HysteresisInterpolator.fromFile("datafile.dat", 0, 1)
print ip(particular_H, direction)
```
`direction` is either positive or negative number that tells the interpolator
which curve so select in terms of rising/falling.

If you want to skip some lines you can add additional parameter `skip` like this:
```python
ip = HysteresisInterpolator.fromFile("gp000.dat", 1, 0, skip=15)
```

