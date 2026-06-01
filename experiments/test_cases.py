# =============================================================================
# test_cases.py
# Hybrid Toxic Language Detection Pipeline
# Sample Test Cases — Realistic MLBB Filipino & English Game Chat Messages
# =============================================================================
# Each test case is a dictionary with:
#   "message"  : raw chat message (as typed by a player)
#   "label"    : "toxic" or "clean"
#   "type"     : category of test case (see TYPE LEGEND below)
#   "note"     : brief description for paper documentation
#
# TYPE LEGEND:
#   plain_toxic     — toxic word in plain text, no obfuscation
#   leet_basic      — Variant 1 obfuscation (vowels + s, t substituted)
#   leet_inter      — Variant 2 obfuscation (adds b→8, g→9, l→1)
#   mixed           — combination of plain and leet in one message
#   codeswitched    — Filipino + English mixed naturally
#   clean           — non-toxic, should NOT be flagged
#
# NOTE ON POSITION:
#   Toxic words appear at the START, MIDDLE, and END of messages
#   to reflect realistic and varied game chat behavior in MLBB.
# =============================================================================
 
test_cases = [
 
    # ------------------------------------------------------------------
    # CATEGORY 1: PLAIN TOXIC — Filipino
    # Toxic word at varied positions. No obfuscation.
    # ------------------------------------------------------------------
    {
        "message": "gago, bakit mo binasag yung tower namin",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at start — tower destruction complaint"
    },
    {
        "message": "pre ang layo ng push mo, bobo",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at end — pushing complaint"
    },
    {
        "message": "bakit ka nag-solo lord, tanga ka ba",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at end — Lord objective complaint"
    },
    {
        "message": "ulol, sinong nagsabi sayo na mag-jungle ka",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at start — role complaint"
    },
    {
        "message": "wala kang silbi sa team, inutil ka talaga",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at end — team contribution insult"
    },
    {
        "message": "tangina, bakit hindi ka nag-rotate sa mid",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at start — rotation complaint"
    },
    {
        "message": "ang tarantado mong support, walang heal",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at middle — support role complaint"
    },
    {
        "message": "report niyo itong feeder, gago talaga",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at end — report request"
    },
    {
        "message": "leche ka, bakit mo ginamit ult ko ng wala",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at start — ultimate ability complaint"
    },
    {
        "message": "sino ang nag-pick ng Franco, putang ina",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at end — hero pick complaint"
    },
 
    # ------------------------------------------------------------------
    # CATEGORY 2: PLAIN TOXIC — English
    # Toxic word at varied positions. No obfuscation.
    # ------------------------------------------------------------------
    {
        "message": "idiot, why did you steal my blue buff",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at start — jungle resource complaint"
    },
    {
        "message": "our jungler is a complete noob, no ganks at all",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at middle — jungler complaint"
    },
    {
        "message": "stop dying every 30 seconds, you are trash",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at end — death frequency complaint"
    },
    {
        "message": "garbage marksman, zero damage all game",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at start — damage output complaint"
    },
    {
        "message": "I carried this moron all game and still lost",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at middle — carry complaint"
    },
    {
        "message": "this support never heals, so useless",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at end — support complaint"
    },
    {
        "message": "feeder detected, report this loser after game",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "multiple toxic words — report threat"
    },
    {
        "message": "brainless play, you walked straight into their tower",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at start — positioning complaint"
    },
    {
        "message": "we have a coward tank who never initiates",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at middle — tank role complaint"
    },
    {
        "message": "how are you this pathetic at level 15",
        "label": "toxic",
        "type": "plain_toxic",
        "note": "toxic word at middle — skill level complaint"
    },
 
    # ------------------------------------------------------------------
    # CATEGORY 3: LEET VARIANT 1 — Filipino (Basic Obfuscation)
    # Vowels + s, t substituted. Toxic word at varied positions.
    # ------------------------------------------------------------------
    {
        "message": "g4g0, bakit ka nag-back habang may teamfight",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at start — backing during teamfight"
    },
    {
        "message": "pre ang tagal mong mag-recall, b0b0 ka",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at end — recalling complaint"
    },
    {
        "message": "sino ang 74ng4 na nag-solo push ng inhibitor",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at middle — solo pushing complaint"
    },
    {
        "message": "ang layo ng posisyon mo pre, ul0l",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at end — positioning complaint"
    },
    {
        "message": "74ng1n4, binenta mo na naman kami sa turtle",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at start — turtle objective complaint"
    },
    {
        "message": "wala kang damage kahit fed ka na, 1nu71l",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at end — damage complaint despite being fed"
    },
    {
        "message": "ang l3ch3 mong mage, puro miss lang ult",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at middle — missing ultimate complaint"
    },
    {
        "message": "report mo na yang p4kyu na support",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at middle — support report request"
    },
    {
        "message": "saan ka nanggaling, kup4l",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at end — general gameplay complaint"
    },
    {
        "message": "duw4g, bakit ka palaging nasa base",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at start — base-hugging complaint"
    },
 
    # ------------------------------------------------------------------
    # CATEGORY 4: LEET VARIANT 1 — English (Basic Obfuscation)
    # ------------------------------------------------------------------
    {
        "message": "1d107, that was our lord buff you just wasted",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at start — Lord buff waste complaint"
    },
    {
        "message": "our marksman is a complete n00b, no positioning",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at middle — marksman positioning complaint"
    },
    {
        "message": "three deaths in two minutes, what a 7r45h player",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at end — early death complaint"
    },
    {
        "message": "f33d3r mage, you gave them three kills already",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at start — kill feeding complaint"
    },
    {
        "message": "this tank build is u53l355, no CC at all",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at middle — build and CC complaint"
    },
    {
        "message": "zero map awareness, absolute d0gw473r jungler",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at end — map awareness complaint"
    },
    {
        "message": "cl0wn picked Yi Sun-shin support, instant loss",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at start — unconventional hero pick complaint"
    },
    {
        "message": "you are such a l053r, get out of my lobby",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at middle — lobby complaint"
    },
    {
        "message": "worst Chou player I have seen, 57up1d combos",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at end — combo execution complaint"
    },
    {
        "message": "w34k damage output, are you even trying",
        "label": "toxic",
        "type": "leet_basic",
        "note": "leet at start — damage output complaint"
    },
 
    # ------------------------------------------------------------------
    # CATEGORY 5: LEET VARIANT 2 — Filipino (Intermediate Obfuscation)
    # Adds b→8, g→9, l→1 substitutions. Varied positions.
    # ------------------------------------------------------------------
    {
        "message": "9490, bakit ka nag-ult ng walang target",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at start — wasted ultimate complaint"
    },
    {
        "message": "pre ang tagal mo sa base, 8080 ka talaga",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at end — base time complaint"
    },
    {
        "message": "yung 74n94 na Layla, puro miss lang",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at middle — Layla marksman complaint"
    },
    {
        "message": "ang layo ng posisyon mo, u101 ka ba",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at end — positioning complaint"
    },
    {
        "message": "74n91n4, binasag mo pa yung inhibitor ng maaga",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at start — inhibitor complaint"
    },
    {
        "message": "wala kang map awareness, 8u4n9 ka talaga",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at end — map awareness complaint"
    },
    {
        "message": "ang 9un990n9 mong Tigreal, walang hook",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at middle — Tigreal tank complaint"
    },
    {
        "message": "8411w ka na ba, three times kang na-lord steal",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at start — Lord steal complaint"
    },
    {
        "message": "kahit fed si Granger, p4n937 pa rin ang gameplay",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at end — Granger performance complaint"
    },
    {
        "message": "845705 ka, ayaw mo pang mag-surrender",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at start — surrender refusal complaint"
    },
 
    # ------------------------------------------------------------------
    # CATEGORY 6: LEET VARIANT 2 — English (Intermediate Obfuscation)
    # ------------------------------------------------------------------
    {
        "message": "1d107 jungler, you gave first blood for free",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at start — first blood complaint"
    },
    {
        "message": "our Harith is a complete n008, zero damage",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at middle — Harith mage complaint"
    },
    {
        "message": "five deaths before minute five, absolute 94r8493",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at end — early game death complaint"
    },
    {
        "message": "8r41n1355 Fanny, you never reach the backline",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at start — Fanny assassin complaint"
    },
    {
        "message": "this Khufra is w0r7h1355, no engage at all",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at middle — Khufra tank complaint"
    },
    {
        "message": "never playing with this 5cru8 again",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at middle — general player complaint"
    },
    {
        "message": "what a f411ur3 of a carry, zero late game",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at middle — late game carry complaint"
    },
    {
        "message": "807 mechanics on Gusion, unbelievable",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at start — Gusion combo complaint"
    },
    {
        "message": "you play Lancelot like a c10wn every single game",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at middle — Lancelot assassin complaint"
    },
    {
        "message": "reported already, stop 9r13f1n9 the ranked game",
        "label": "toxic",
        "type": "leet_inter",
        "note": "leet at end — griefing report"
    },
 
    # ------------------------------------------------------------------
    # CATEGORY 7: MIXED — Plain + Leet in one message
    # ------------------------------------------------------------------
    {
        "message": "gago ka talaga, ur such an 1d107 in teamfight",
        "label": "toxic",
        "type": "mixed",
        "note": "Filipino plain at start + English leet at middle"
    },
    {
        "message": "ang layo ng rotate mo, b0b0 at bobo ka pa",
        "label": "toxic",
        "type": "mixed",
        "note": "same word in leet and plain in same message"
    },
    {
        "message": "stop feeding the enemy Ling, 57up1d tanga ka",
        "label": "toxic",
        "type": "mixed",
        "note": "English leet + Filipino plain at end"
    },
    {
        "message": "n00b ka pre, gago ka pa, grabe talaga",
        "label": "toxic",
        "type": "mixed",
        "note": "English leet at start + Filipino plain at middle"
    },
    {
        "message": "74ng4 ka at trash ka pa, sino nagturo sayo",
        "label": "toxic",
        "type": "mixed",
        "note": "Filipino leet at start + English plain at middle"
    },
 
    # ------------------------------------------------------------------
    # CATEGORY 8: CODE-SWITCHED — Natural MLBB Filipino + English
    # ------------------------------------------------------------------
    {
        "message": "hoy 74ng4 mo, why are you not rotating to turtle",
        "label": "toxic",
        "type": "codeswitched",
        "note": "leet at middle — turtle objective rotation complaint"
    },
    {
        "message": "grabe ka, such a n00b, report na kita after",
        "label": "toxic",
        "type": "codeswitched",
        "note": "leet at middle — report threat"
    },
    {
        "message": "ang b0b0 ng jungler natin, zero gank the whole game",
        "label": "toxic",
        "type": "codeswitched",
        "note": "leet at middle — jungler gank complaint"
    },
    {
        "message": "why are you taking my blue buff, 9490 ka",
        "label": "toxic",
        "type": "codeswitched",
        "note": "leet at end — jungle resource complaint"
    },
    {
        "message": "inutil ka, you are so useless in every teamfight",
        "label": "toxic",
        "type": "codeswitched",
        "note": "plain at start — teamfight contribution complaint"
    },
    {
        "message": "1d107 ka pre, paulit ulit kang namamatay sa same spot",
        "label": "toxic",
        "type": "codeswitched",
        "note": "leet at start — repeated death at same location"
    },
    {
        "message": "you missed every hook this game, 74ng4 talaga",
        "label": "toxic",
        "type": "codeswitched",
        "note": "leet at end — hook accuracy complaint"
    },
    {
        "message": "trash ka pre, bakit ka pa nag-ranked kung ganyan ka",
        "label": "toxic",
        "type": "codeswitched",
        "note": "plain at start — ranked mode complaint"
    },
    {
        "message": "sino ang 8080 na nag-pick ng Odette sa ranked",
        "label": "toxic",
        "type": "codeswitched",
        "note": "leet at middle — hero pick complaint"
    },
    {
        "message": "lagi kang late sa teamfight, loser ka talaga",
        "label": "toxic",
        "type": "codeswitched",
        "note": "plain at end — teamfight timing complaint"
    },
 
    # ------------------------------------------------------------------
    # CATEGORY 9: CLEAN MESSAGES — Should NOT be flagged
    # Realistic MLBB cooperative and sportsmanship messages.
    # ------------------------------------------------------------------
    {
        "message": "good game everyone, GG WP",
        "label": "clean",
        "type": "clean",
        "note": "standard end-of-game sportsmanship"
    },
    {
        "message": "mag-rotate na sa bottom, malapit na silang mag-push",
        "label": "clean",
        "type": "clean",
        "note": "Filipino rotation callout"
    },
    {
        "message": "focus the Ling first before the Esmeralda",
        "label": "clean",
        "type": "clean",
        "note": "English target priority callout"
    },
    {
        "message": "penge heal pre, halos mamatay na ako",
        "label": "clean",
        "type": "clean",
        "note": "Filipino heal request"
    },
    {
        "message": "lets secure the turtle before they respawn",
        "label": "clean",
        "type": "clean",
        "note": "English objective coordination"
    },
    {
        "message": "nice shot Layla, galing mo",
        "label": "clean",
        "type": "clean",
        "note": "positive compliment to marksman"
    },
    {
        "message": "farming muna ako, kulang pa items ko",
        "label": "clean",
        "type": "clean",
        "note": "Filipino farming callout"
    },
    {
        "message": "wait for me, respawn in 5 seconds then we push",
        "label": "clean",
        "type": "clean",
        "note": "English respawn coordination"
    },
    {
        "message": "ingat kayo sa bush, may naka-ambush doon",
        "label": "clean",
        "type": "clean",
        "note": "Filipino ambush warning"
    },
    {
        "message": "I will go tank build to protect the carry",
        "label": "clean",
        "type": "clean",
        "note": "English build announcement"
    },
    {
        "message": "GG pre, close game talaga yan",
        "label": "clean",
        "type": "clean",
        "note": "code-switched GG message"
    },
    {
        "message": "let us group up at lord pit at 12 minutes",
        "label": "clean",
        "type": "clean",
        "note": "English Lord objective timing callout"
    },
    {
        "message": "susuportahan kita sa teamfight, mag-engage ka na",
        "label": "clean",
        "type": "clean",
        "note": "Filipino support engagement callout"
    },
    {
        "message": "back muna tayo, kulang pa HP natin para mag-lord",
        "label": "clean",
        "type": "clean",
        "note": "Filipino retreat and health management callout"
    },
    {
        "message": "nice defense guys, we held that push well",
        "label": "clean",
        "type": "clean",
        "note": "English positive reinforcement after defense"
    },
]
 
# =============================================================================
# SUMMARY STATISTICS
# =============================================================================
if __name__ == "__main__":
    total = len(test_cases)
    toxic = sum(1 for t in test_cases if t["label"] == "toxic")
    clean = sum(1 for t in test_cases if t["label"] == "clean")
 
    types = {}
    for t in test_cases:
        types[t["type"]] = types.get(t["type"], 0) + 1
 
    print("=" * 60)
    print("TEST CASE SUMMARY — MLBB Game Chat")
    print("=" * 60)
    print(f"Total test cases : {total}")
    print(f"Toxic messages   : {toxic}")
    print(f"Clean messages   : {clean}")
    print()
    print("Breakdown by type:")
    for k, v in sorted(types.items()):
        print(f"  {k:<20} : {v}")
    print("=" * 60)