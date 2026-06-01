# =============================================================================
# hybrid.py
# Hybrid Toxic Language Detection Pipeline
# Component 4 — Hybrid Pipeline Orchestrator
# =============================================================================
# Integrates the Leetspeak Normalizer, Boyer-Moore (Stage 1), and
# Aho-Corasick (Stage 2) into a unified two-stage detection pipeline.
#
# Pipeline Flow:
#   Raw Message
#     → [Stage 0] Leetspeak Normalization
#     → [Stage 1] Boyer-Moore Pre-Screen (high-risk keywords only)
#         └── No match → EARLY TERMINATION (message is clean)
#         └── Match found → proceed to Stage 2
#     → [Stage 2] Aho-Corasick Full Dictionary Scan
#     → Deduplicated match results
#
# Design Decisions:
#   - Trie is built ONCE during HybridPipeline initialization
#   - Boyer-Moore iterates over high-risk keyword subset (not full dict)
#   - Early termination saves Aho-Corasick cost on clean messages
#   - All outputs are structured dicts for downstream use
# =============================================================================
 
import time
import tracemalloc
 
from normalizer    import normalize
from boyer_moore   import boyer_moore_scan, HIGH_RISK_KEYWORDS
from aho_corasick  import build_trie, build_failure_links, aho_corasick_scan_prebuilt
 
 
# =============================================================================
# HYBRID PIPELINE CLASS
# Encapsulates the full pipeline with a pre-built trie for efficiency.
# =============================================================================
class HybridPipeline:
    """
    Orchestrates the three-stage hybrid toxic language detection pipeline.
 
    Attributes:
        dictionary       (list)     : Full toxic word dictionary
        high_risk        (list)     : Curated high-risk keyword subset for BM
        root             (TrieNode) : Pre-built Aho-Corasick trie (built once)
    """
 
    def __init__(self, dictionary: list, high_risk_keywords: list = None):
        """
        Initializes the pipeline. Builds the Aho-Corasick trie ONCE.
 
        Parameters:
            dictionary         (list): Full toxic word dictionary
            high_risk_keywords (list): Subset for Boyer-Moore pre-screen.
                                       Defaults to HIGH_RISK_KEYWORDS from
                                       boyer_moore.py if not provided.
        """
        self.dictionary = [w.lower().strip() for w in dictionary if w.strip()]
        self.high_risk  = high_risk_keywords if high_risk_keywords else HIGH_RISK_KEYWORDS
 
        # Build Aho-Corasick trie once — reused across all messages
        self.root = build_trie(self.dictionary)
        self.root = build_failure_links(self.root)
 
 
    # -------------------------------------------------------------------------
    # CORE METHOD — Process a single raw message
    # -------------------------------------------------------------------------
    def process(self, raw_message: str) -> dict:
        """
        Runs the full hybrid pipeline on a single raw chat message.
 
        Parameters:
            raw_message (str): Raw game chat message as typed by the player
 
        Returns:
            dict: Structured detection result with the following fields:
                  - raw_text        (str)  : Original input
                  - normalized_text (str)  : After leetspeak normalization
                  - flagged         (bool) : True if toxic content detected
                  - stage_triggered (str)  : 'none', 'bm_only', or 'bm+ac'
                  - bm_matches      (list) : Boyer-Moore stage matches
                  - ac_matches      (list) : Aho-Corasick stage matches
                  - matches         (list) : Final deduplicated match list
                                            [{"pattern", "start_index", "end_index"}]
        """
        # --- Stage 0: Normalization -------------------------------------------
        normalized = normalize(raw_message)
 
        # --- Stage 1: Boyer-Moore Pre-Screen ----------------------------------
        bm_raw = boyer_moore_scan(normalized, self.high_risk)
 
        if not bm_raw:
            # Early termination — no high-risk keyword found
            return {
                "raw_text"        : raw_message,
                "normalized_text" : normalized,
                "flagged"         : False,
                "stage_triggered" : "none",
                "bm_matches"      : [],
                "ac_matches"      : [],
                "matches"         : [],
            }
 
        # --- Stage 2: Aho-Corasick Full Dictionary Scan ----------------------
        ac_raw = aho_corasick_scan_prebuilt(normalized, self.root)
 
        # --- Deduplication and formatting ------------------------------------
        all_matches = _merge_and_format(bm_raw, ac_raw, normalized)
 
        return {
            "raw_text"        : raw_message,
            "normalized_text" : normalized,
            "flagged"         : len(all_matches) > 0,
            "stage_triggered" : "bm+ac",
            "bm_matches"      : bm_raw,
            "ac_matches"      : ac_raw,
            "matches"         : all_matches,
        }
 
 
    # -------------------------------------------------------------------------
    # BATCH METHOD — Process a list of messages
    # -------------------------------------------------------------------------
    def process_batch(self, messages: list) -> list:
        """
        Processes a list of raw chat messages through the full pipeline.
 
        Parameters:
            messages (list): List of raw chat message strings
 
        Returns:
            list: List of structured detection result dicts (one per message)
        """
        return [self.process(msg) for msg in messages]
 
 
    # -------------------------------------------------------------------------
    # TIMED METHOD — Process a single message with latency tracking
    # -------------------------------------------------------------------------
    def process_timed(self, raw_message: str) -> dict:
        """
        Same as process(), but also measures wall-clock execution time.
 
        Returns:
            dict: Detection result with an additional 'processing_time_us' field
                  (time in microseconds)
        """
        start  = time.perf_counter()
        result = self.process(raw_message)
        end    = time.perf_counter()
 
        result["processing_time_us"] = round((end - start) * 1_000_000, 3)
        return result
 
 
# =============================================================================
# STANDALONE FUNCTION — One-shot scan without class initialization
# Useful for quick testing; less efficient for bulk runs.
# =============================================================================
def hybrid_scan(raw_message: str, dictionary: list,
                high_risk_keywords: list = None) -> dict:
    """
    One-shot hybrid scan. Builds the trie on every call — use for testing only.
    For production/benchmarking, use HybridPipeline class (trie built once).
 
    Parameters:
        raw_message        (str) : Raw chat message
        dictionary         (list): Full toxic word dictionary
        high_risk_keywords (list): Subset for BM pre-screen. Defaults to
                                   HIGH_RISK_KEYWORDS from boyer_moore.py.
 
    Returns:
        dict: Same structured result as HybridPipeline.process()
    """
    pipeline = HybridPipeline(dictionary, high_risk_keywords)
    return pipeline.process(raw_message)
 
 
# =============================================================================
# HELPER — Merge BM and AC results, deduplicate, and reformat
# =============================================================================
def _merge_and_format(bm_raw: list, ac_raw: list, text: str) -> list:
    """
    Merges Boyer-Moore and Aho-Corasick match lists, deduplicates on
    (keyword, position) pairs, and reformats into a flat list of match dicts.
 
    Parameters:
        bm_raw (list): Raw BM match list  [{keyword, positions}, ...]
        ac_raw (list): Raw AC match list  [{keyword, positions}, ...]
        text   (str) : Normalized text (used to compute end_index)
 
    Returns:
        list: Deduplicated match list:
              [{"pattern": str, "start_index": int, "end_index": int}, ...]
    """
    seen    = set()
    results = []
 
    # Flatten BM and AC matches into unified (keyword, start) tuples
    for entry in bm_raw + ac_raw:
        keyword = entry["keyword"]
        for pos in entry["positions"]:
            key = (keyword, pos)
            if key not in seen:
                seen.add(key)
                results.append({
                    "pattern"    : keyword,
                    "start_index": pos,
                    "end_index"  : pos + len(keyword) - 1,
                })
 
    # Sort by position for consistent output
    results.sort(key=lambda x: x["start_index"])
    return results
 
 
# =============================================================================
# PRETTY PRINTER — Console-friendly result display
# =============================================================================
def print_result(result: dict) -> None:
    """
    Prints a formatted detection result to stdout.
 
    Parameters:
        result (dict): Output from HybridPipeline.process() or hybrid_scan()
    """
    print("-" * 65)
    print(f"  Raw Text       : {result['raw_text']}")
    print(f"  Normalized     : {result['normalized_text']}")
    print(f"  Flagged        : {result['flagged']}")
    print(f"  Stage Triggered: {result['stage_triggered']}")
 
    if result["matches"]:
        print(f"  Matches ({len(result['matches'])}):")
        for m in result["matches"]:
            print(f"    → '{m['pattern']}' at index {m['start_index']}–{m['end_index']}")
    else:
        print("  Matches        : None")
 
    if "processing_time_us" in result:
        print(f"  Time (µs)      : {result['processing_time_us']}")
    print("-" * 65)
 
 
# =============================================================================
# QUICK TEST — run this file directly to verify the hybrid pipeline
# =============================================================================
if __name__ == "__main__":
 
    # Sample dictionary — in production this is loaded from the dataset
    SAMPLE_DICTIONARY = [
        "gago", "bobo", "tanga", "ulol", "tangina", "putang ina",
        "puta", "leche", "gaga", "kupal", "hindot", "punyeta",
        "pakyu", "hayop", "buwisit", "lintik", "tae", "suso",
        "animal", "peste", "retard", "cancer", "die", "autism",
        "cripple", "delete yourself", "get out", "inutil", "idiot",
        "stupid", "noob", "trash", "lodi", "basura",
    ]
 
    pipeline = HybridPipeline(SAMPLE_DICTIONARY)
 
    test_cases = [
        # (raw_message,                   should_flag)
        ("ang g4g0 mo pre",               True),   # leetspeak gago
        ("b0b0 ka talaga",                True),   # leetspeak bobo
        ("74ng4 naman oh",                True),   # leetspeak tanga
        ("$7up1d ka",                     True),   # leetspeak stupid
        ("ul0l na to",                    True),   # leetspeak ulol
        ("putang ina mo",                 True),   # direct match multi-word
        ("good game everyone",            False),  # clean message
        ("nice kill bro",                 False),  # clean message
        ("ang gago mo, bobo ka talaga",   True),   # multiple matches
        ("GG WP",                         False),  # clean, uppercase
        ("74ng1n4 mo pre",                True),   # leetspeak tangina
        ("",                              False),  # empty
        ("delete yourself noob",          True),   # English harassment
        ("1d107 ka",                      True),   # leetspeak idiot
    ]
 
    print("=" * 65)
    print("HYBRID PIPELINE TEST RESULTS")
    print("=" * 65)
    print(f"{'Raw Input':<35} {'Expected':<10} {'Got':<10} {'Pass'}")
    print("-" * 65)
 
    all_passed = True
    for raw, expected_flag in test_cases:
        result = pipeline.process_timed(raw)
        got    = result["flagged"]
        passed = got == expected_flag
        if not passed:
            all_passed = False
        status = "✅" if passed else "❌"
        print(f"{raw:<35} {str(expected_flag):<10} {str(got):<10} {status}")
 
    print("-" * 65)
    if all_passed:
        print("All tests passed. Hybrid pipeline is working correctly.")
    else:
        print("Some tests failed. Review pipeline logic.")
    print("=" * 65)
 
    # Detailed view of a sample result
    print("\nDETAILED EXAMPLE:")
    detail = pipeline.process_timed("ang g4g0 mo, sobrang b0b0 talaga")
    print_result(detail)