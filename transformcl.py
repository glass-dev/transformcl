"""Transform angular power spectra."""

__all__ = [
    "cl",
    "corr",
    "theta",
    "var",
]

from array_api_compat import array_namespace

import flt


def corr(cl, closed=False):
    r"""
    Transform angular power spectrum to angular correlation function.

    Takes an angular power spectrum with :math:`\mathtt{n} =
    \mathtt{lmax}+1` coefficients and returns the corresponding angular
    correlation function in :math:`\mathtt{n}` points.

    The correlation function values can be computed either over the
    closed interval :math:`[0, \pi]`, in which case :math:`\theta_0 = 0`
    and :math:`\theta_{n-1} = \pi`, or over the open interval :math:`(0,
    \pi)`.

    Parameters
    ----------
    cl : (n,) array_like
        Angular power spectrum from :math:`0` to :math:`\mathtt{lmax}`.
    closed : bool
        Compute correlation function over open (``closed=False``) or closed
        (``closed=True``) interval.

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

    xp = array_namespace(cl)

    # length n of the transform
    if cl.ndim != 1:
        raise TypeError("cl must be 1d array")
    n = cl.shape[-1]

    # DLT coefficients = (2l+1)/(4pi) * Cl
    a = (2 * xp.arange(n) + 1) / (4 * xp.pi) * cl

    return flt.idlt(a, closed)


def cl(corr, closed=False):
    r"""
    Transform angular correlation function to angular power spectrum.

    Takes an angular function in :math:`\mathtt{n}` points and returns
    the corresponding angular power spectrum from :math:`0` to
    :math:`\mathtt{lmax} = \mathtt{n}-1`.

    The correlation function must be given at the angles returned by
    :func:`transformcl.theta`.  These can be distributed either over the
    closed interval :math:`[0, \pi]`, in which case :math:`\theta_0 = 0`
    and :math:`\theta_{n-1} = \pi`, or over the open interval :math:`(0,
    \pi)`.

    Parameters
    ----------
    corr : (n,) array_like
        Angular correlation function.

    Returns
    -------
    cl : (n,) array_like
        Angular power spectrum from :math:`0` to :math:`\mathtt{lmax}`.
    closed : bool
        Compute correlation function over open (``closed=False``) or
        closed (``closed=True``) interval.

    See Also
    --------
    transformcl.corr :
        the inverse operation
    transformcl.theta :
        angles at which the correlation function is evaluated

    """

    xp = array_namespace(corr)

    # length n of the transform
    if corr.ndim != 1:
        raise TypeError("corr must be 1d array")
    n = corr.shape[-1]

    # DLT coefficients = (2l+1)/(4pi) * Cl
    fl = (2 * xp.arange(n) + 1) / (4 * xp.pi)

    return flt.dlt(corr, closed) / fl


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


def theta(n, closed=False):
    r"""
    Return the angles :math:`\theta_1, \ldots, \theta_n` of the
    correlation function with *n* points.
    """
    return flt.theta(n, closed)


cltocorr = corr
corrtocl = cl
cltovar = var
