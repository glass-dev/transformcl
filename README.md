# transformcl

**Transform angular power spectra and correlation functions.**

This is a minimal Python package for transformations between angular power
spectra and correlation functions. It is currently limited to the spin zero
case.

The package can be installed using pip:

    pip install transformcl

Then import the package to use the functions:

```py
import transformcl
t = transformcl.theta(cl.size)
ct = transformcl.corr(cl)
```

For more information, please see the [documentation].

Current functionality covers the absolutely minimal use case. Please open an
issue on GitHub if you would like to see anything added.

[documentation]: https://glass.readthedocs.io/projects/transformcl/latest
