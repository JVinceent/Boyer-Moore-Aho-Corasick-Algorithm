# =============================================================================
# __init__.py
# Hybrid Toxic Language Detection Pipeline
# =============================================================================
# Exposes the top-level public API for the pipeline package.
# Import the HybridPipeline class and utility functions directly from here.
#
# Usage:
#   from hybrid_pipeline import HybridPipeline, normalize, hybrid_scan
# =============================================================================

from normalizer   import normalize, normalize_batch, LEET_MAP
from boyer_moore  import boyer_moore_search, boyer_moore_scan, HIGH_RISK_KEYWORDS
from aho_corasick import build_trie, build_failure_links, aho_corasick_search
from hybrid       import HybridPipeline, hybrid_scan, print_result

__version__ = "1.0.0"
__authors__  = [
    "Doria, John Vincent",
    "Estil, Susan Marie",
    "Fanoga, Haidie N.",
    "Guillo, Rejc C.",
    "Hepuller, Kate Nicole",
]
__course__  = "Design and Analysis of Algorithms"
__school__  = "Batangas State University – Alangilan Campus"

__all__ = [
    "HybridPipeline",
    "hybrid_scan",
    "normalize",
    "normalize_batch",
    "LEET_MAP",
    "boyer_moore_search",
    "boyer_moore_scan",
    "HIGH_RISK_KEYWORDS",
    "build_trie",
    "build_failure_links",
    "aho_corasick_search",
    "print_result",
]
