"""Transform angular power spectra."""

__all__ = [
    "backend",
    "cl",
    "corr",
    "theta",
    "use",
    "var",
]

from contextlib import contextmanager
from typing import Literal

from array_api_compat import array_namespace

BackendStr = Literal[
    "flt-ii",
    "flt-i",
]


backend: BackendStr = "flt-ii"
"""Backend for transforms. See :ref:`backends`."""


@contextmanager
def use(choice: BackendStr) -> None:
    """Context manager to change backend. See :ref:`backends`."""
    global backend
    restore = backend
    backend = choice
    try:
        yield
    finally:
        backend = restore


def corr(cl):
    r"""
    Transform angular power spectrum to angular correlation function.

    Takes an angular power spectrum with :math:`\mathtt{n} =
    \mathtt{lmax}+1` coefficients and returns the corresponding angular
    correlation function in :math:`\mathtt{n}` points.

    The correlation function is computed at the angles returned by
    :func:`transformcl.theta`.

    Parameters
    ----------
    cl : (n,) array_like
        Angular power spectrum from :math:`0` to :math:`\mathtt{lmax}`.

    Returns
    -------
    corr : (n,) array_like
        Angular correlation function.

    See Also
    --------
    transformcl.cl :
        the inverse operation
    transformcl.theta :
        angles at which the correlation function is evaluated

    """

    # length n of the transform
    if cl.ndim != 1:
        raise TypeError("cl must be 1d array")
    n = cl.shape[-1]

    if backend in ["flt-ii", "flt-i"]:
        xp = array_namespace(cl)
        # DLT coefficients = (2l+1)/(4pi) * Cl
        a = (2 * xp.arange(n) + 1) / (4 * xp.pi) * cl

        if backend == "flt-ii":
            import flt

            return flt.idlt(a)

        if backend == "flt-i":
            import flt

            return flt.idlt(a, True)

    raise NotImplementedError(f"unknown backend {backend!r}")


def cl(corr):
    r"""
    Transform angular correlation function to angular power spectrum.

    Takes an angular function in :math:`\mathtt{n}` points and returns
    the corresponding angular power spectrum from :math:`0` to
    :math:`\mathtt{lmax} = \mathtt{n}-1`.

    The correlation function must be given at the angles returned by
    :func:`transformcl.theta`.

    Parameters
    ----------
    corr : (n,) array_like
        Angular correlation function.

    Returns
    -------
    cl : (n,) array_like
        Angular power spectrum from :math:`0` to :math:`\mathtt{lmax}`.

    See Also
    --------
    transformcl.corr :
        the inverse operation
    transformcl.theta :
        angles at which the correlation function is evaluated

    """

    # length n of the transform
    if corr.ndim != 1:
        raise TypeError("corr must be 1d array")
    n = corr.shape[-1]

    if backend in ["flt-ii", "flt-i"]:
        xp = array_namespace(corr)
        # DLT coefficients = (2l+1)/(4pi) * Cl
        fl = (2 * xp.arange(n) + 1) / (4 * xp.pi)

        if backend == "flt-ii":
            import flt

            return flt.dlt(corr) / fl

        if backend == "flt-i":
            import flt

            return flt.dlt(corr, True) / fl

    raise NotImplementedError(f"unknown backend {backend!r}")


def var(cl):
    r"""
    Compute variance from angular power spectrum.

    Given the angular power spectrum, compute the variance of the
    spherical random field in a point.

    Parameters
    ----------
    cl : array_like
        Angular power spectrum.  Can be multidimensional, with the last
        axis representing the modes.

    Returns
    -------
    var: float
        The variance of the given power spectrum.

    Notes
    -----
    The variance :math:`\sigma^2` of the field with power spectrum
    :math:`C_l` is

    .. math::

        \sigma^2 = \sum_{l} \frac{2l + 1}{4\pi} \, C_l \;.

    """
    xp = array_namespace(cl)
    ell = xp.arange(cl.shape[-1])
    return xp.sum((2 * ell + 1) / (4 * xp.pi) * cl, axis=-1)


def theta(n):
    r"""
    Return the angles :math:`\theta_1, \ldots, \theta_n` of the
    correlation function with *n* points.
    """

    if backend == "flt-ii":
        import flt

        return flt.theta(n)
    if backend == "flt-i":
        import flt

        return flt.theta(n, True)

    raise NotImplementedError(f"unknown backend {backend!r}")


cltocorr = corr
corrtocl = cl
cltovar = var
