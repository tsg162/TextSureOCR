"""
Integration tests for OCR digit-for-letter substitution detection.

Covers six common OCR confusions where digits are misread as letters:
  0 -> o,  1 -> l,  3 -> e,  5 -> s,  7 -> t,  8 -> b

~4,800 parametrized cases total.  Each test sends corrupted text to the
live service and asserts the error is detected, the corrupted span is
returned, and the correct word appears in suggestions.
"""

import pytest
from helpers import ocr_check

# ═══════════════════════════════════════════════════════════════════════
# 1.  Zero for O  (0 → o)   — 120 words × 10 templates = 1,200 tests
# ═══════════════════════════════════════════════════════════════════════

ZERO_FOR_O_WORDS = list(dict.fromkeys([
    "brown", "police", "computer", "morning", "document", "control",
    "problem", "solution", "company", "operation", "position", "condition",
    "production", "population", "protection", "construction", "corporation",
    "direction", "collection", "convention", "motion", "ocean", "rocket",
    "pocket", "doctor", "factor", "motor", "monitor", "governor",
    "professor", "color", "honor", "labor", "mirror", "terror", "error",
    "author", "donor", "humor", "junior", "senior", "corridor", "warrior",
    "senator", "location", "modern", "moment", "money", "month", "morning",
    "model", "moreover", "motion", "mount", "noble", "normal", "north",
    "note", "nothing", "notice", "novel", "object", "observe", "office",
    "option", "order", "other", "outside", "over", "phone", "photo",
    "policy", "polite", "political", "poor", "popular", "portion",
    "positive", "possible", "power", "prior", "process", "produce",
    "profit", "program", "project", "promise", "promote", "proper",
    "propose", "protect", "prove", "provide", "protocol", "reason",
    "record", "reform", "report", "resource", "response", "role", "room",
    "root", "round", "school", "score", "short", "social", "solid",
    "solution", "story", "strong", "total", "tone", "tool", "topic",
    "touch", "tower", "voice", "volume", "vote", "woman", "wonder",
    "world", "worry", "worth",
]))

ZERO_FOR_O_TEMPLATES = [
    "The {word} was mentioned in the official report yesterday",
    "She carefully examined the {word} before making her decision",
    "According to the latest findings, the {word} played a crucial role",
    "They discovered that the {word} had changed significantly over time",
    "The researchers analyzed the {word} and published their results",
    "In the final paragraph, the {word} was described in great detail",
    "Several experts agreed that the {word} needed further investigation",
    "During the meeting, the {word} became a major point of discussion",
    "The committee reviewed the {word} as part of the annual assessment",
    "Historical records indicate that the {word} dates back centuries",
]


def _generate_zero_for_o():
    cases = []
    for word in ZERO_FOR_O_WORDS:
        idx = word.find("o")
        if idx == -1:
            continue
        corrupted = word[:idx] + "0" + word[idx + 1:]
        for ti, template in enumerate(ZERO_FOR_O_TEMPLATES, start=1):
            text = template.format(word=corrupted)
            test_id = f"0_for_o__{corrupted}__t{ti}"
            cases.append((text, corrupted, word, test_id))
    return cases


_RAW_ZERO_FOR_O = _generate_zero_for_o()

# ═══════════════════════════════════════════════════════════════════════
# 2.  One for L  (1 → l)   — 100 words × 10 templates = 1,000 tests
# ═══════════════════════════════════════════════════════════════════════

ONE_FOR_L_WORDS = [
    "letter", "hello", "people", "school", "build", "cable", "plain",
    "table", "simple", "little", "global", "metal", "legal", "level",
    "local", "moral", "final", "total", "royal", "vital", "label",
    "model", "panel", "novel", "angel", "camel", "hotel", "rebel",
    "cancel", "channel", "travel", "tunnel", "animal", "capital",
    "central", "crystal", "digital", "federal", "general", "hospital",
    "journal", "liberal", "literal", "magical", "martial", "medical",
    "mineral", "minimal", "musical", "natural", "neutral", "nominal",
    "normal", "optical", "orbital", "partial", "personal", "physical",
    "plural", "political", "principal", "professional", "proposal",
    "protocol", "radical", "rational", "regional", "removal", "renewal",
    "rental", "seasonal", "several", "signal", "social", "special",
    "spiritual", "surgical", "survival", "terminal", "thermal",
    "tropical", "typical", "universal", "vertical", "virtual", "visual",
    "approval", "arrival", "colonial", "commercial", "conditional",
    "constitutional", "conventional", "criminal", "cultural", "emotional",
    "environmental", "essential", "eventual", "external",
]

ONE_FOR_L_TEMPLATES = [
    "The {word} arrived at the main office this morning",
    "We need to update the {word} before the deadline",
    "The inspector verified the {word} during the routine check",
    "Everyone agreed that the {word} was handled properly",
    "The report mentioned the {word} several times throughout",
    "After careful review, the {word} was approved by the board",
    "The new {word} was introduced at the conference last week",
    "Scientists studied the {word} under controlled conditions",
    "The {word} proved essential for the success of the project",
    "Management decided to prioritize the {word} going forward",
]


def _generate_one_for_l():
    cases = []
    for word in ONE_FOR_L_WORDS:
        idx = word.find("l")
        if idx == -1:
            continue
        corrupted = word[:idx] + "1" + word[idx + 1:]
        for ti, template in enumerate(ONE_FOR_L_TEMPLATES, start=1):
            text = template.format(word=corrupted)
            test_id = f"1_for_l__{corrupted}__t{ti}"
            cases.append((text, corrupted, word, test_id))
    return cases


_RAW_ONE_FOR_L = _generate_one_for_l()

# ═══════════════════════════════════════════════════════════════════════
# 3.  Three for E  (3 → e)   — 80 words × 10 templates = 800 tests
# ═══════════════════════════════════════════════════════════════════════

THREE_FOR_E_WORDS = [
    "better", "between", "before", "behind", "benefit", "believe",
    "beyond", "career", "center", "complete", "create", "debate",
    "decrease", "defense", "degree", "deliver", "demand", "describe",
    "design", "desire", "determine", "develop", "device", "different",
    "direct", "disease", "dream", "economy", "education", "effect",
    "effort", "election", "element", "emerge", "energy", "engine",
    "entire", "environment", "episode", "equal", "escape", "establish",
    "event", "every", "evidence", "example", "excellent", "exercise",
    "expect", "expense", "experience", "experiment", "expert", "express",
    "extend", "extreme", "federal", "finance", "freedom", "frequent",
    "general", "heritage", "increase", "interest", "internet", "leader",
    "measure", "member", "message", "method", "network", "never",
    "perfect", "person", "preserve", "prevent", "recent", "remember",
    "research", "resource",
]

THREE_FOR_E_TEMPLATES = [
    "The {word} was thoroughly discussed at the annual conference",
    "Many people considered the {word} to be extremely important",
    "The government announced changes to the {word} policy",
    "Researchers published a comprehensive study about the {word}",
    "The organization focused its efforts on improving the {word}",
    "After the review, the {word} was modified to meet new standards",
    "The {word} significantly impacted the outcome of the project",
    "Experts recommended paying closer attention to the {word}",
    "The recent developments regarding the {word} surprised everyone",
    "Students were required to understand the {word} before proceeding",
]


def _generate_three_for_e():
    cases = []
    for word in THREE_FOR_E_WORDS:
        idx = word.find("e")
        if idx == -1:
            continue
        corrupted = word[:idx] + "3" + word[idx + 1:]
        for ti, template in enumerate(THREE_FOR_E_TEMPLATES, start=1):
            text = template.format(word=corrupted)
            test_id = f"3_for_e__{corrupted}__t{ti}"
            cases.append((text, corrupted, word, test_id))
    return cases


_RAW_THREE_FOR_E = _generate_three_for_e()

# ═══════════════════════════════════════════════════════════════════════
# 4.  Five for S  (5 → s)   — 70 words × 10 templates = 700 tests
# ═══════════════════════════════════════════════════════════════════════

FIVE_FOR_S_WORDS = [
    "school", "system", "science", "social", "simple", "single", "small",
    "solid", "south", "space", "special", "stable", "standard", "state",
    "station", "steel", "stock", "stone", "store", "story", "street",
    "strong", "student", "study", "style", "subject", "success", "summer",
    "supply", "support", "surface", "survey", "sweet", "symbol", "master",
    "message", "mission", "missing", "monster", "muscle", "sister",
    "season", "section", "second", "secret", "secure", "select", "senior",
    "sense", "series", "serve", "session", "settle", "severe", "signal",
    "silent", "silver", "skill", "sleep", "solution", "source", "spirit",
    "spring", "square", "stage", "statement", "steady", "straight",
    "strange", "strategy",
]

FIVE_FOR_S_TEMPLATES = [
    "The {word} was recognized as one of the finest in the country",
    "Parents were concerned about the quality of the {word}",
    "The new {word} attracted widespread attention from the media",
    "Officials announced improvements to the existing {word}",
    "The {word} had been operating successfully for many years",
    "Residents praised the {word} for its outstanding performance",
    "The {word} underwent significant changes during the renovation",
    "Analysts predicted strong growth for the {word} sector",
    "The {word} was featured prominently in the documentary",
    "Community leaders emphasized the importance of the {word}",
]


def _generate_five_for_s():
    cases = []
    for word in FIVE_FOR_S_WORDS:
        idx = word.find("s")
        if idx == -1:
            continue
        corrupted = word[:idx] + "5" + word[idx + 1:]
        for ti, template in enumerate(FIVE_FOR_S_TEMPLATES, start=1):
            text = template.format(word=corrupted)
            test_id = f"5_for_s__{corrupted}__t{ti}"
            cases.append((text, corrupted, word, test_id))
    return cases


_RAW_FIVE_FOR_S = _generate_five_for_s()

# ═══════════════════════════════════════════════════════════════════════
# 5.  Seven for T  (7 → t)   — 60 words × 10 templates = 600 tests
# ═══════════════════════════════════════════════════════════════════════

SEVEN_FOR_T_WORDS = [
    "table", "talent", "target", "taste", "teacher", "technology",
    "temperature", "temple", "terminal", "territory", "test", "theater",
    "theory", "therapy", "thought", "title", "together", "tomorrow",
    "total", "touch", "tourist", "tower", "tradition", "traffic",
    "training", "transfer", "transport", "travel", "treatment", "treaty",
    "trend", "trial", "tribute", "trouble", "trust", "truth", "tunnel",
    "battle", "better", "bottom", "butter", "button", "captain",
    "cartoon", "castle", "cattle", "center", "chapter", "content",
    "context", "control", "cotton", "counter", "country", "custom",
    "digital", "distant", "eastern", "fifteen", "gentle",
]

SEVEN_FOR_T_TEMPLATES = [
    "The {word} was established decades ago in the heart of the city",
    "Visitors were impressed by the remarkable {word} on display",
    "The professor lectured extensively about the {word} topic",
    "Local authorities invested heavily in modernizing the {word}",
    "The {word} received an award for excellence this year",
    "Historians traced the origins of the {word} to ancient times",
    "The documentary explored every aspect of the {word} in depth",
    "Funding for the {word} was approved by the legislative body",
    "The {word} played a pivotal role in shaping the community",
    "Engineers redesigned the {word} to improve overall efficiency",
]


def _generate_seven_for_t():
    cases = []
    for word in SEVEN_FOR_T_WORDS:
        idx = word.find("t")
        if idx == -1:
            continue
        corrupted = word[:idx] + "7" + word[idx + 1:]
        for ti, template in enumerate(SEVEN_FOR_T_TEMPLATES, start=1):
            text = template.format(word=corrupted)
            test_id = f"7_for_t__{corrupted}__t{ti}"
            cases.append((text, corrupted, word, test_id))
    return cases


_RAW_SEVEN_FOR_T = _generate_seven_for_t()

# ═══════════════════════════════════════════════════════════════════════
# 6.  Eight for B  (8 → b)   — 50 words × 10 templates = 500 tests
# ═══════════════════════════════════════════════════════════════════════

EIGHT_FOR_B_WORDS = [
    "balance", "bank", "base", "basic", "battle", "beach", "beauty",
    "become", "before", "begin", "behind", "belief", "belong", "below",
    "benefit", "best", "better", "between", "beyond", "blood", "board",
    "body", "bond", "book", "border", "born", "bottom", "bound", "brain",
    "branch", "brand", "brave", "bread", "break", "bridge", "brief",
    "bright", "bring", "broad", "broken", "brother", "brown", "budget",
    "build", "burden", "burn", "business", "cabinet", "cable", "carbon",
]

EIGHT_FOR_B_TEMPLATES = [
    "The {word} was examined under strict laboratory conditions",
    "The annual report highlighted the importance of the {word}",
    "Experts debated the significance of the {word} at the summit",
    "The {word} remained intact despite the challenging circumstances",
    "Observers noted that the {word} had improved considerably",
    "The {word} was central to the discussion at the town hall",
    "Researchers confirmed that the {word} met all safety standards",
    "The {word} attracted considerable interest from investors",
    "The {word} was carefully documented for future reference",
    "Environmental studies revealed new insights about the {word}",
]


def _generate_eight_for_b():
    cases = []
    for word in EIGHT_FOR_B_WORDS:
        idx = word.find("b")
        if idx == -1:
            continue
        corrupted = word[:idx] + "8" + word[idx + 1:]
        for ti, template in enumerate(EIGHT_FOR_B_TEMPLATES, start=1):
            text = template.format(word=corrupted)
            test_id = f"8_for_b__{corrupted}__t{ti}"
            cases.append((text, corrupted, word, test_id))
    return cases


_RAW_EIGHT_FOR_B = _generate_eight_for_b()

# ═══════════════════════════════════════════════════════════════════════
# Combine all raw cases and build the parametrize list
# ═══════════════════════════════════════════════════════════════════════

RAW_CASES = (
    _RAW_ZERO_FOR_O
    + _RAW_ONE_FOR_L
    + _RAW_THREE_FOR_E
    + _RAW_FIVE_FOR_S
    + _RAW_SEVEN_FOR_T
    + _RAW_EIGHT_FOR_B
)

# Strip the test-id column for the parametrize values; ids come separately.
CASES = [(text, err, corr) for text, err, corr, _ in RAW_CASES]


# ═══════════════════════════════════════════════════════════════════════
# The single parametrized test
# ═══════════════════════════════════════════════════════════════════════


@pytest.mark.integration
@pytest.mark.ocr_positive
@pytest.mark.parametrize(
    "text,error_word,correction",
    CASES,
    ids=[c[3] for c in RAW_CASES],
)
def test_ocr_digit_substitution(text, error_word, correction, api):
    """Verify the service detects a digit-for-letter OCR substitution."""
    body = ocr_check(api, text)
    assert body["result"] == "issue_detected", (
        f"Expected issue_detected for '{error_word}' in: {text}"
    )
    span_texts = {s["text"] for s in body.get("spans", [])}
    assert error_word in span_texts, (
        f"Missing span for '{error_word}'"
    )
    if correction:
        span = next(s for s in body["spans"] if s["text"] == error_word)
        sugg_texts = {s["text"].lower() for s in span.get("suggestions", [])}
        assert correction.lower() in sugg_texts, (
            f"Missing suggestion '{correction}' for '{error_word}'"
        )
