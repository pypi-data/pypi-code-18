"""
Provide a common place to access pmf-based divergences.

"""
from .jensen_shannon_divergence import (
    jensen_shannon_divergence_pmf as jensen_shannon_divergence
)

from ._kl_nonmerge import (
    cross_entropy_pmf as cross_entropy,
    relative_entropy_pmf as relative_entropy
)

