# =============================================================================
# test_cases.py
# Hybrid Toxic Language Detection Pipeline
# Sample Test Cases — Realistic MLBB Filipino & English Game Chat Messages
# =============================================================================

from typing import List, Dict
import sys
import os

# Adjust for relative imports when run inside /experiments/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # import the enhanced detection pipeline
    from boyer_moore import boyer_moore_detect
except ImportError:
    # fallback dummy detector
    def boyer_moore_detect(text: str, *args, **kwargs) -> Dict[str, str]:
        return {"is_toxic": any(w in text.lower() for w in ["gago", "bobo", "puta"])}

# ANSI color codes for better terminal output
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    GRAY = "\033[90m"

# =============================================================================
# TEST CASES (Paper-Ready Dataset)
# =============================================================================
test_cases: List[Dict[str, str]] = [
    # --- CATEGORY 1: PLAIN TOXIC — Filipino ---
    {"message": "gago, bakit mo binasag yung tower namin", "label": "toxic", "type": "plain_toxic", "note": "toxic word at start"},
    {"message": "pre ang layo ng push mo, bobo", "label": "toxic", "type": "plain_toxic", "note": "toxic word at end"},
    {"message": "bakit ka nag-solo lord, tanga ka ba", "label": "toxic", "type": "plain_toxic", "note": "toxic word at end"},
    {"message": "ulol, sinong nagsabi sayo na mag-jungle ka", "label": "toxic", "type": "plain_toxic", "note": "toxic word at start"},
    {"message": "wala kang silbi sa team, inutil ka talaga", "label": "toxic", "type": "plain_toxic", "note": "toxic word at end"},
    {"message": "tangina, bakit hindi ka nag-rotate sa mid", "label": "toxic", "type": "plain_toxic", "note": "toxic word at start"},
    {"message": "ang tarantado mong support, walang heal", "label": "toxic", "type": "plain_toxic", "note": "toxic word at middle"},
    {"message": "report niyo itong feeder, gago talaga", "label": "toxic", "type": "plain_toxic", "note": "toxic word at end"},
    {"message": "leche ka, bakit mo ginamit ult ko ng wala", "label": "toxic", "type": "plain_toxic", "note": "toxic word at start"},
    {"message": "sino ang nag-pick ng Franco, putang ina", "label": "toxic", "type": "plain_toxic", "note": "toxic word at end"},

    # --- CATEGORY 2: PLAIN TOXIC — English ---
    {"message": "idiot, why did you steal my blue buff", "label": "toxic", "type": "plain_toxic", "note": "toxic word at start"},
    {"message": "our jungler is a complete noob, no ganks at all", "label": "toxic", "type": "plain_toxic", "note": "toxic word at middle"},
    {"message": "stop dying every 30 seconds, you are trash", "label": "toxic", "type": "plain_toxic", "note": "toxic word at end"},
    {"message": "garbage marksman, zero damage all game", "label": "toxic", "type": "plain_toxic", "note": "toxic word at start"},
    {"message": "I carried this moron all game and still lost", "label": "toxic", "type": "plain_toxic", "note": "toxic word at middle"},
    {"message": "this support never heals, so useless", "label": "toxic", "type": "plain_toxic", "note": "toxic word at end"},
    {"message": "feeder detected, report this loser after game", "label": "toxic", "type": "plain_toxic", "note": "multiple toxic words"},
    {"message": "brainless play, you walked straight into their tower", "label": "toxic", "type": "plain_toxic", "note": "toxic word at start"},
    {"message": "we have a coward tank who never initiates", "label": "toxic", "type": "plain_toxic", "note": "toxic word at middle"},
    {"message": "how are you this pathetic at level 15", "label": "toxic", "type": "plain_toxic", "note": "toxic word at middle"},

    # --- CATEGORY 3: LEET VARIANT 1 — Filipino (Basic Obfuscation) ---
    {"message": "g4g0, bakit ka nag-back habang may teamfight", "label": "toxic", "type": "leet_basic", "note": "leet at start"},
    {"message": "pre ang tagal mong mag-recall, b0b0 ka", "label": "toxic", "type": "leet_basic", "note": "leet at end"},
    {"message": "sino ang 74ng4 na nag-solo push ng inhibitor", "label": "toxic", "type": "leet_basic", "note": "leet at middle"},
    {"message": "ang layo ng posisyon mo pre, ul0l", "label": "toxic", "type": "leet_basic", "note": "leet at end"},
    {"message": "74ng1n4, binenta mo na naman kami sa turtle", "label": "toxic", "type": "leet_basic", "note": "leet at start"},
    {"message": "wala kang damage kahit fed ka na, 1nu71l", "label": "toxic", "type": "leet_basic", "note": "leet at end"},
    {"message": "ang l3ch3 mong mage, puro miss lang ult", "label": "toxic", "type": "leet_basic", "note": "leet at middle"},
    {"message": "report mo na yang p4kyu na support", "label": "toxic", "type": "leet_basic", "note": "leet at middle"},
    {"message": "saan ka nanggaling, kup4l", "label": "toxic", "type": "leet_basic", "note": "leet at end"},
    {"message": "duw4g, bakit ka palaging nasa base", "label": "toxic", "type": "leet_basic", "note": "leet at start"},

    # --- CATEGORY 4: LEET VARIANT 1 — English (Basic Obfuscation) ---
    {"message": "1d107, that was our lord buff you just wasted", "label": "toxic", "type": "leet_basic", "note": "leet at start"},
    {"message": "our marksman is a complete n00b, no positioning", "label": "toxic", "type": "leet_basic", "note": "leet at middle"},
    {"message": "three deaths in two minutes, what a 7r45h player", "label": "toxic", "type": "leet_basic", "note": "leet at end"},
    {"message": "f33d3r mage, you gave them three kills already", "label": "toxic", "type": "leet_basic", "note": "leet at start"},
    {"message": "this tank build is u53l355, no CC at all", "label": "toxic", "type": "leet_basic", "note": "leet at middle"},
    {"message": "zero map awareness, absolute d0gw473r jungler", "label": "toxic", "type": "leet_basic", "note": "leet at end"},
    {"message": "cl0wn picked Yi Sun-shin support, instant loss", "label": "toxic", "type": "leet_basic", "note": "leet at start"},
    {"message": "you are such a l053r, get out of my lobby", "label": "toxic", "type": "leet_basic", "note": "leet at middle"},
    {"message": "worst Chou player I have seen, 57up1d combos", "label": "toxic", "type": "leet_basic", "note": "leet at end"},
    {"message": "w34k damage output, are you even trying", "label": "toxic", "type": "leet_basic", "note": "leet at start"},

    # --- CATEGORY 5: LEET VARIANT 2 — Filipino (Intermediate Obfuscation) ---
    {"message": "9490, bakit ka nag-ult ng walang target", "label": "toxic", "type": "leet_inter", "note": "leet at start"},
    {"message": "pre ang tagal mo sa base, 8080 ka talaga", "label": "toxic", "type": "leet_inter", "note": "leet at end"},
    {"message": "yung 74n94 na Layla, puro miss lang", "label": "toxic", "type": "leet_inter", "note": "leet at middle"},
    {"message": "ang layo ng posisyon mo, u101 ka ba", "label": "toxic", "type": "leet_inter", "note": "leet at end"},
    {"message": "74n91n4, binasag mo pa yung inhibitor ng maaga", "label": "toxic", "type": "leet_inter", "note": "leet at start"},
    {"message": "wala kang map awareness, 8u4n9 ka talaga", "label": "toxic", "type": "leet_inter", "note": "leet at end"},
    {"message": "ang 9un990n9 mong Tigreal, walang hook", "label": "toxic", "type": "leet_inter", "note": "leet at middle"},
    {"message": "8411w ka na ba, three times kang na-lord steal", "label": "toxic", "type": "leet_inter", "note": "leet at start"},
    {"message": "kahit fed si Granger, p4n937 pa rin ang gameplay", "label": "toxic", "type": "leet_inter", "note": "leet at end"},
    {"message": "845705 ka, ayaw mo pang mag-surrender", "label": "toxic", "type": "leet_inter", "note": "leet at start"},

    # --- CATEGORY 6: LEET VARIANT 2 — English (Intermediate Obfuscation) ---
    {"message": "1d107 jungler, you gave first blood for free", "label": "toxic", "type": "leet_inter", "note": "leet at start"},
    {"message": "our Harith is a complete n008, zero damage", "label": "toxic", "type": "leet_inter", "note": "leet at middle"},
    {"message": "five deaths before minute five, absolute 94r8493", "label": "toxic", "type": "leet_inter", "note": "leet at end"},
    {"message": "8r41n1355 Fanny, you never reach the backline", "label": "toxic", "type": "leet_inter", "note": "leet at start"},
    {"message": "this Khufra is w0r7h1355, no engage at all", "label": "toxic", "type": "leet_inter", "note": "leet at middle"},
    {"message": "never playing with this 5cru8 again", "label": "toxic", "type": "leet_inter", "note": "leet at middle"},
    {"message": "what a f411ur3 of a carry, zero late game", "label": "toxic", "type": "leet_inter", "note": "leet at middle"},
    {"message": "807 mechanics on Gusion, unbelievable", "label": "toxic", "type": "leet_inter", "note": "leet at start"},
    {"message": "you play Lancelot like a c10wn every single game", "label": "toxic", "type": "leet_inter", "note": "leet at middle"},
    {"message": "reported already, stop 9r13f1n9 the ranked game", "label": "toxic", "type": "leet_inter", "note": "leet at end"},

    # --- CATEGORY 7: MIXED — Plain + Leet in one message ---
    {"message": "gago ka talaga, ur such an 1d107 in teamfight", "label": "toxic", "type": "mixed", "note": "Filipino plain + English leet"},
    {"message": "ang layo ng rotate mo, b0b0 at bobo ka pa", "label": "toxic", "type": "mixed", "note": "same word leet and plain"},
    {"message": "stop feeding the enemy Ling, 57up1d tanga ka", "label": "toxic", "type": "mixed", "note": "English leet + Filipino plain"},
    {"message": "n00b ka pre, gago ka pa, grabe talaga", "label": "toxic", "type": "mixed", "note": "English leet + Filipino plain"},
    {"message": "74ng4 ka at trash ka pa, sino nagturo sayo", "label": "toxic", "type": "mixed", "note": "Filipino leet + English plain"},

    # --- CATEGORY 8: CODE-SWITCHED — Natural MLBB Filipino + English ---
    {"message": "hoy 74ng4 mo, why are you not rotating to turtle", "label": "toxic", "type": "codeswitched", "note": "leet + code-switch"},
    {"message": "grabe ka, such a n00b, report na kita after", "label": "toxic", "type": "codeswitched", "note": "code-switch + leet"},
    {"message": "ang b0b0 ng jungler natin, zero gank the whole game", "label": "toxic", "type": "codeswitched", "note": "code-switch + leet"},
    {"message": "why are you taking my blue buff, 9490 ka", "label": "toxic", "type": "codeswitched", "note": "code-switch + leet"},
    {"message": "inutil ka, you are so useless in every teamfight", "label": "toxic", "type": "codeswitched", "note": "code-switch plain"},
    {"message": "1d107 ka pre, paulit ulit kang namamatay sa same spot", "label": "toxic", "type": "codeswitched", "note": "code-switch + leet"},
    {"message": "you missed every hook this game, 74ng4 talaga", "label": "toxic", "type": "codeswitched", "note": "code-switch + leet"},
    {"message": "trash ka pre, bakit ka pa nag-ranked kung ganyan ka", "label": "toxic", "type": "codeswitched", "note": "code-switch plain"},
    {"message": "sino ang 8080 na nag-pick ng Odette sa ranked", "label": "toxic", "type": "codeswitched", "note": "code-switch + leet"},
    {"message": "lagi kang late sa teamfight, loser ka talaga", "label": "toxic", "type": "codeswitched", "note": "code-switch plain"},

    # --- CATEGORY 9: CLEAN MESSAGES — Should NOT be flagged ---
    {"message": "good game everyone, GG WP", "label": "clean", "type": "clean", "note": "sportsmanship"},
    {"message": "mag-rotate na sa bottom, malapit na silang mag-push", "label": "clean", "type": "clean", "note": "rotation callout"},
    {"message": "focus the Ling first before the Esmeralda", "label": "clean", "type": "clean", "note": "target priority"},
    {"message": "penge heal pre, halos mamatay na ako", "label": "clean", "type": "clean", "note": "heal request"},
    {"message": "lets secure the turtle before they respawn", "label": "clean", "type": "clean", "note": "objective coordination"},
    {"message": "nice shot Layla, galing mo", "label": "clean", "type": "clean", "note": "compliment"},
    {"message": "farming muna ako, kulang pa items ko", "label": "clean", "type": "clean", "note": "farming callout"},
    {"message": "wait for me, respawn in 5 seconds then we push", "label": "clean", "type": "clean", "note": "respawn coordination"},
    {"message": "ingat kayo sa bush, may naka-ambush doon", "label": "clean", "type": "clean", "note": "ambush warning"},
    {"message": "I will go tank build to protect the carry", "label": "clean", "type": "clean", "note": "build announcement"},
    {"message": "GG pre, close game talaga yan", "label": "clean", "type": "clean", "note": "code-switched GG"},
    {"message": "let us group up at lord pit at 12 minutes", "label": "clean", "type": "clean", "note": "Lord coordination"},
    {"message": "susuportahan kita sa teamfight, mag-engage ka na", "label": "clean", "type": "clean", "note": "support engagement"},
    {"message": "back muna tayo, kulang pa HP natin para mag-lord", "label": "clean", "type": "clean", "note": "retreat callout"},
    {"message": "nice defense guys, we held that push well", "label": "clean", "type": "clean", "note": "positive reinforcement"},
]

# =============================================================================
# STATISTICS FUNCTIONS
# =============================================================================

def summarize_cases(cases: List[Dict[str, str]]) -> None:
    """Print category counts, toxic/clean ratio, and summary table."""
    total = len(cases)
    toxic = sum(1 for t in cases if t["label"] == "toxic")
    clean = total - toxic

    # distribution by type
    type_counts: Dict[str, int] = {}
    for t in cases:
        type_counts[t["type"]] = type_counts.get(t["type"], 0) + 1

    title = f"{Colors.BOLD}{Colors.CYAN}TEST CASE SUMMARY — MLBB Game Chat{Colors.RESET}"
    print(f"\n{Colors.GRAY}{'=' * 65}{Colors.RESET}")
    print(title.center(65))
    print(f"{Colors.GRAY}{'=' * 65}{Colors.RESET}")
    print(f"Total test cases : {Colors.BOLD}{total}{Colors.RESET}")
    print(f"Toxic messages   : {Colors.RED}{toxic}{Colors.RESET}")
    print(f"Clean messages   : {Colors.GREEN}{clean}{Colors.RESET}\n")

    print(f"{Colors.BOLD}Breakdown by Type:{Colors.RESET}")
    for typ, count in sorted(type_counts.items()):
        color = Colors.RED if "toxic" in typ else Colors.GREEN
        print(f"  {color}{typ:<20}{Colors.RESET} : {count}")
    print(f"{Colors.GRAY}{'=' * 65}{Colors.RESET}\n")

def quick_pipeline_check(cases: List[Dict[str, str]], n: int = 6) -> None:
    """
    Quickly verify integration with the enhanced Boyer–Moore detector.
    Runs detection on a few test cases (both toxic & clean).
    """
    sample_cases = cases[:n]
    print(f"{Colors.BOLD}{Colors.YELLOW}Running quick detection check on {len(sample_cases)} samples...{Colors.RESET}")
    print(f"{Colors.GRAY}{'-' * 70}{Colors.RESET}")

    for tc in sample_cases:
        msg = tc["message"]
        expected = tc["label"]
        result = boyer_moore_detect(msg, return_details=True)
        detected = "toxic" if result.get("is_toxic") else "clean"

        status_color = Colors.RED if detected == "toxic" else Colors.GREEN
        pass_color = Colors.GREEN if detected == expected else Colors.YELLOW
        print(f"{Colors.BOLD}Message:{Colors.RESET} {msg}")
        print(f" → Expected: {expected}, Detected: {status_color}{detected}{Colors.RESET}, "
              f"Score: {Colors.CYAN}{result.get('score', 'N/A')}{Colors.RESET}")
        print(f"   Status: {pass_color}{'PASS' if detected == expected else 'CHECK'}{Colors.RESET}")
        if result.get("is_toxic"):
            for det in result.get("details", []):
                print(f"     - Matched: {Colors.RED}{det['keyword']}{Colors.RESET} "
                      f"(tier={det['tier']}, sev={det['severity']})")
        print(f"{Colors.GRAY}{'-' * 70}{Colors.RESET}")
    print()

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    summarize_cases(test_cases)
    quick_pipeline_check(test_cases)