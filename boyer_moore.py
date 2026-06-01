# =============================================================================
# boyer_moore.py
# Hybrid Toxic Language Detection Pipeline
# Component 2 — Boyer-Moore Algorithm
# =============================================================================
# Implements the Boyer-Moore string matching algorithm using both the
# Bad Character Heuristic and Good Suffix Heuristic. In the hybrid pipeline,
# Boyer-Moore serves as the first pattern matching stage — a fast pre-screen
# against a curated set of high-risk keywords. If no high-risk keyword is
# found, the pipeline terminates early without proceeding to Aho-Corasick.
#
# Design Decisions:
#   - Operates on normalized, lowercased text only (output of normalizer.py)
#   - Uses substring matching (no word boundary restriction)
#   - Returns match positions for documentation and benchmarking
#   - Iterates over each keyword independently (single-pattern by design)
# =============================================================================
 
 
# =============================================================================
# HIGH-RISK KEYWORD LIST
# Derived from Profanity (Tier 1) and Harassment (Tier 2) categories
# of the toxic word dataset. These are the most severe and frequently
# occurring toxic terms in MLBB Filipino and English game chat.
# =============================================================================
HIGH_RISK_KEYWORDS = [
    # --- Filipino Profanity (Tier 1) ---
    "gago", "bobo", "tanga", "ulol", "tangina", "putang ina",
    "puta", "leche", "gaga", "kupal", "hindot", "punyeta",
    "pakyu", "hayop", "buwisit", "lintik", "tae", "suso",
    "animal", "peste",
 
    # --- English Harassment (Tier 2) ---
    "retard", "cancer", "die", "autism", "cripple",
    "delete yourself", "get out",
]
 
 
# =============================================================================
# PREPROCESSING — BAD CHARACTER TABLE
# =============================================================================
def build_bad_character_table(pattern: str) -> dict:
    """
    Builds the bad character table for a given pattern.
    Maps each character in the pattern to its rightmost index.
    On a mismatch, this table tells Boyer-Moore how far to shift
    the pattern to align the mismatched text character with its
    last occurrence in the pattern.
 
    Parameters:
        pattern (str): The keyword to search for
 
    Returns:
        dict: Character → rightmost index in pattern
    """
    table = {}
    for i, char in enumerate(pattern):
        table[char] = i
    return table
 
 
# =============================================================================
# PREPROCESSING — GOOD SUFFIX TABLE
# =============================================================================
def build_good_suffix_table(pattern: str) -> list:
    """
    Builds the good suffix shift table for a given pattern.
    When a mismatch occurs after partial matches, this table determines
    how far to shift the pattern based on the already-matched suffix,
    preventing redundant re-examination of matched characters.
 
    Parameters:
        pattern (str): The keyword to search for
 
    Returns:
        list: Array of shift values indexed by mismatch position
    """
    m = len(pattern)
    shift = [m] * (m + 1)
    border = [0] * (m + 1)
 
    i = m
    j = m + 1
    border[i] = j
 
    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == m:
                shift[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j
 
    j = border[0]
    for i in range(m + 1):
        if shift[i] == m:
            shift[i] = j
        if i == j:
            j = border[j]
 
    return shift
 
 
# =============================================================================
# CORE SEARCH — SINGLE PATTERN
# =============================================================================
def boyer_moore_search(text: str, pattern: str) -> list:
    """
    Searches for a single pattern in the normalized text using
    the Boyer-Moore algorithm with both Bad Character and Good
    Suffix heuristics. At each mismatch, takes the larger of the
    two shift values to maximize characters skipped.
 
    Parameters:
        text    (str): Normalized chat message (output of normalizer.py)
        pattern (str): Single keyword to search for
 
    Returns:
        list: List of starting indices where the pattern was found.
              Empty list if no match found.
    """
    if not text or not pattern:
        return []
 
    n = len(text)
    m = len(pattern)
 
    if m > n:
        return []
 
    # Build preprocessing tables
    bad_char   = build_bad_character_table(pattern)
    good_suffix = build_good_suffix_table(pattern)
 
    matches = []
    i = 0  # current position in text
 
    while i <= n - m:
        j = m - 1  # start comparing from rightmost character of pattern
 
        # Compare right to left
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
 
        if j < 0:
            # Full match found at position i
            matches.append(i)
            i += good_suffix[0]
        else:
            # Mismatch — apply both heuristics, take the larger shift
            bad_char_shift  = j - bad_char.get(text[i + j], -1)
            good_suffix_shift = good_suffix[j + 1]
            i += max(bad_char_shift, good_suffix_shift)
 
    return matches
 
 
# =============================================================================
# PIPELINE FUNCTION — SCAN ALL HIGH-RISK KEYWORDS
# =============================================================================
def boyer_moore_scan(text: str, keywords: list = None) -> list:
    """
    Scans the normalized text against all high-risk keywords by
    invoking boyer_moore_search() once per keyword. Collects all
    matches across all keywords and returns them as a unified list.
 
    This is the function called by hybrid.py in Stage 1.
 
    Parameters:
        text     (str) : Normalized chat message
        keywords (list): List of keywords to scan against.
                         Defaults to HIGH_RISK_KEYWORDS if not provided.
 
    Returns:
        list: List of dicts — each containing the matched keyword
              and the positions where it was found.
              Empty list if no high-risk keyword detected.
 
    Example return value:
        [
            {"keyword": "gago", "positions": [4]},
            {"keyword": "bobo", "positions": [13]}
        ]
    """
    if keywords is None:
        keywords = HIGH_RISK_KEYWORDS
 
    results = []
 
    for keyword in keywords:
        positions = boyer_moore_search(text, keyword)
        if positions:
            results.append({
                "keyword"  : keyword,
                "positions": positions
            })
 
    return results
 
 
# =============================================================================
# STANDALONE SCAN — Used for benchmarking Boyer-Moore alone
# Same as boyer_moore_scan but accepts a full dictionary instead of
# just high-risk keywords. This allows fair comparison with Aho-Corasick
# in the experimental results section.
# =============================================================================
def boyer_moore_full_scan(text: str, dictionary: list) -> list:
    """
    Scans normalized text against a full dictionary of toxic words.
    Used exclusively in benchmark.py to evaluate standalone Boyer-Moore
    performance against the complete toxic word list — simulating what
    Boyer-Moore alone would look like without Aho-Corasick support.
 
    Parameters:
        text       (str) : Normalized chat message
        dictionary (list): Full list of toxic words from dataset
 
    Returns:
        list: All matches found across the full dictionary
    """
    results = []
 
    for keyword in dictionary:
        positions = boyer_moore_search(text, keyword)
        if positions:
            results.append({
                "keyword"  : keyword,
                "positions": positions
            })
 
    return results
 
 
# =============================================================================
# QUICK TEST — run this file directly to verify Boyer-Moore is working
# =============================================================================
if __name__ == "__main__":
 
    print("=" * 65)
    print("BOYER-MOORE TEST RESULTS")
    print("=" * 65)
 
    test_cases = [
        # (normalized_text, pattern, expected_positions)
        ("ang gago mo",              "gago",       [4]),
        ("bobo ka talaga",           "bobo",        [0]),
        ("pre ang bobo mo",          "bobo",        [8]),
        ("wala kang silbi inutil",   "inutil",      [15]),
        ("good game everyone",       "gago",        []),   # clean — no match
        ("gagogago",                 "gago",        [0, 4]),  # multiple matches
        ("ang gago mo bobo ka",      "bobo",        [11]),
        ("",                         "gago",        []),   # empty text
        ("gago",                     "",            []),   # empty pattern
    ]
 
    all_passed = True
    print(f"{'Text':<30} {'Pattern':<12} {'Expected':<15} {'Result':<15} {'Pass'}")
    print("-" * 65)
 
    for text, pattern, expected in test_cases:
        result = boyer_moore_search(text, pattern)
        passed = result == expected
        if not passed:
            all_passed = False
        status = "✅" if passed else "❌"
        print(f"{text:<30} {pattern:<12} {str(expected):<15} {str(result):<15} {status}")
 
    print("-" * 65)
 
    # Test the full scanner with high-risk keywords
    print("\nTesting boyer_moore_scan() with high-risk keywords:")
    print("-" * 65)
    sample = "ang gago mo, sobrang bobo talaga ng support natin"
    scan_result = boyer_moore_scan(sample)
    print(f"Input   : '{sample}'")
    print(f"Matches : {scan_result}")
 
    print("-" * 65)
    if all_passed:
        print("All tests passed. Boyer-Moore is working correctly.")
    else:
        print("Some tests failed. Review the implementation.")
    print("=" * 65)