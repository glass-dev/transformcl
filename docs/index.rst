:mod:`transformcl` --- Transform angular power spectra
======================================================

This is a minimal Python package for transformations between angular power
spectra and correlation functions.  It is currently limited to the spin zero
case.

The package can be installed using pip::

    pip install transformcl

Then import the package to use the functions::

    import transformcl
    t = transformcl.theta(cl.size)
    ct = transformcl.corr(cl)

Current functionality covers the absolutely minimal use case.  Please open an
issue on GitHub if you would like to see anything added.


.. _backends:

Backends
--------
The :mod:`transformcl` module supports multiple transform backends.  The
current backend can be changed globally by assigning to
:data:`transformcl.backend`::

    transformcl.backend = "<choice>"
    ...

or using the :func:`transformcl.use` context manager::

    with transformcl.use("<choice>"):
        ...

The following backends are available:

.. data:: transformcl.backend
   :value: "flt-ii"
   :no-index:

   The "open" Discrete Legendre Transform (DLT) as implemented by the
   :doc:`flt:index` package, with correlation function values over the open
   interval :math:`(0, \pi)`.

   .. note:: This is the default backend. It supports multiple array types.

.. data:: transformcl.backend
   :value: "flt-i"
   :no-index:

   The "closed" Discrete Legendre Transform (DLT) as implemented by the
   :doc:`flt:index` package, with correlation function values over the closed
   interval :math:`[0, \pi]`.

   .. caution:: This transform should be used with care.  The correlation
      function values are computed all the way to :math:`\theta = 0` from a
      finite bandlimited angular power spectrum.


Reference
---------

.. autodata:: transformcl.backend
.. autofunction:: transformcl.use
.. autofunction:: transformcl.theta
.. autofunction:: transformcl.corr
.. autofunction:: transformcl.cl
.. autofunction:: transformcl.var
