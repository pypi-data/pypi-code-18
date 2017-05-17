r"""

Expectation Propagation
^^^^^^^^^^^^^^^^^^^^^^^

Introduction
------------

This module implements the building-blocks for EP inference: EP parameter
fitting, log of the marginal likelihood, and derivative of the log of the
marginal likelihood.

Private interface
-----------------
"""

from .ep import EP

__all__ = ['EP']
