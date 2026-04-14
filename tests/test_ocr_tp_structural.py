"""
Structural OCR error detection integration tests.

Categories:
  1. Character confusions  (~800 tests)
  2. Transpositions         (~600 tests)
  3. Multi-error texts      (~400 tests)
  4. Hard / tricky cases    (~400 tests)

Total: ~2,200 parameterised cases.
"""

import pytest
from helpers import ocr_check


# ═══════════════════════════════════════════════════════════════════════
# 1. CHARACTER CONFUSIONS  (~800 tests)
# ═══════════════════════════════════════════════════════════════════════

# ── 1a. rn → m  confusion  (38 words × 5 templates = 190 tests) ──────

_RN_M_WORDS = [
    ("governrnent", "government"),
    ("rnanner", "manner"),
    ("rnorning", "morning"),
    ("surnrner", "summer"),
    ("cornrnand", "command"),
    ("cornrnercial", "commercial"),
    ("cornrnitrnent", "commitment"),
    ("cornrnon", "common"),
    ("cornrnunity", "community"),
    ("cornrnent", "comment"),
    ("cornrnunication", "communication"),
    ("cornrnission", "commission"),
    ("recornrnend", "recommend"),
    ("deterrnine", "determine"),
    ("perrnanent", "permanent"),
    ("tournarment", "tournament"),
    ("environrnent", "environment"),
    ("departrment", "department"),
    ("developrnent", "development"),
    ("fundarmental", "fundamental"),
    ("instrurnent", "instrument"),
    ("monurnent", "monument"),
    ("rnoment", "moment"),
    ("norrnal", "normal"),
    ("anirnai", "animal"),
    ("crirninal", "criminal"),
    ("rninirnal", "minimal"),
    ("terrninal", "terminal"),
    ("forrnal", "formal"),
    ("rnental", "mental"),
    ("rernoval", "removal"),
    ("rnaterial", "material"),
    ("rnineral", "mineral"),
    ("therrnal", "thermal"),
    ("rnernorial", "memorial"),
    ("nurnerical", "numerical"),
    ("experirnental", "experimental"),
    ("elernent", "element"),
]

_RN_M_TEMPLATES = [
    "The {word} issued a formal statement regarding the matter",
    "Citizens were asked to review the {word} before the vote",
    "The changes to the {word} affected thousands of residents",
    "A detailed analysis of the {word} was published last month",
    "The new policy regarding the {word} takes effect immediately",
]

CHAR_RN_M_CASES = []
for ocr_word, correct_word in _RN_M_WORDS:
    for tidx, tpl in enumerate(_RN_M_TEMPLATES, 1):
        text = tpl.format(word=ocr_word)
        test_id = f"rn_m_{correct_word}_t{tidx}"
        CHAR_RN_M_CASES.append((text, ocr_word, correct_word, test_id))


# ── 1b. cl → d  confusion  (28 words × 5 templates = 140 tests) ──────

_CL_D_WORDS = [
    ("indude", "include"),
    ("dedare", "declare"),
    ("exdude", "exclude"),
    ("condude", "conclude"),
    ("redaim", "reclaim"),
    ("dedine", "decline"),
    ("disdose", "disclose"),
    ("endose", "enclose"),
    ("prodaim", "proclaim"),
    ("addaim", "acclaim"),
    ("indine", "incline"),
    ("reduse", "recluse"),
    ("nudear", "nuclear"),
    ("cirdular", "circular"),
    ("partidular", "particular"),
    ("spectadular", "spectacular"),
    ("moledular", "molecular"),
    ("musdular", "muscular"),
    ("sedular", "secular"),
    ("artide", "article"),
    ("vehicde", "vehicle"),
    ("mirade", "miracle"),
    ("obstade", "obstacle"),
    ("chronide", "chronicle"),
    ("tentade", "tentacle"),
    ("orade", "oracle"),
    ("spectade", "spectacle"),
    ("partide", "particle"),
]

_CL_D_TEMPLATES = [
    "The report was designed to {word} all relevant information",
    "They decided to {word} the findings from the public record",
    "The committee voted to {word} the new provisions",
    "Experts attempted to {word} the source of the discrepancy",
    "The document was meant to {word} the complete set of rules",
]

CHAR_CL_D_CASES = []
for ocr_word, correct_word in _CL_D_WORDS:
    for tidx, tpl in enumerate(_CL_D_TEMPLATES, 1):
        text = tpl.format(word=ocr_word)
        test_id = f"cl_d_{correct_word}_t{tidx}"
        CHAR_CL_D_CASES.append((text, ocr_word, correct_word, test_id))


# ── 1c. vv → w  confusion  (20 words × 5 templates = 100 tests) ──────

_VV_W_WORDS = [
    ("povver", "power"),
    ("tovver", "tower"),
    ("lovver", "lower"),
    ("flovver", "flower"),
    ("shovver", "shower"),
    ("hovvever", "however"),
    ("ovvner", "owner"),
    ("tovvn", "town"),
    ("brovvn", "brown"),
    ("crovvn", "crown"),
    ("dovvn", "down"),
    ("drovvn", "drown"),
    ("frovvn", "frown"),
    ("grovvn", "grown"),
    ("knovvn", "known"),
    ("shovvn", "shown"),
    ("throvvn", "thrown"),
    ("vvindow", "window"),
    ("vvinter", "winter"),
    ("vvisdom", "wisdom"),
]

_VV_W_TEMPLATES = [
    "The {word} structure was visible from miles away",
    "Construction of the {word} began in the early nineteenth century",
    "The architect designed the {word} to withstand severe weather",
    "Photographs of the {word} appeared in several publications",
    "The restoration of the {word} cost millions of dollars",
]

CHAR_VV_W_CASES = []
for ocr_word, correct_word in _VV_W_WORDS:
    for tidx, tpl in enumerate(_VV_W_TEMPLATES, 1):
        text = tpl.format(word=ocr_word)
        test_id = f"vv_w_{correct_word}_t{tidx}"
        CHAR_VV_W_CASES.append((text, ocr_word, correct_word, test_id))


# ── 1d. l / I  (ell / capital-i) confusion  (20 words × 5 = 100) ─────

_LI_WORDS = [
    ("Iine", "line"),
    ("Iist", "list"),
    ("Iive", "live"),
    ("Iink", "link"),
    ("Iight", "light"),
    ("IittIe", "little"),
    ("Iike", "like"),
    ("Iand", "land"),
    ("Iast", "last"),
    ("Iate", "late"),
    ("Iead", "lead"),
    ("Iearn", "learn"),
    ("Ieave", "leave"),
    ("IegaI", "legal"),
    ("IeveI", "level"),
    ("Iimit", "limit"),
    ("Iisten", "listen"),
    ("IocaI", "local"),
    ("Iunch", "lunch"),
    ("Iarge", "large"),
]

_LI_TEMPLATES = [
    "The new {word} was added to the system database",
    "Staff members reviewed every {word} in the document",
    "The updated {word} included several important changes",
    "Management approved the revised {word} unanimously",
    "The final version of the {word} was distributed to all teams",
]

CHAR_LI_CASES = []
for ocr_word, correct_word in _LI_WORDS:
    for tidx, tpl in enumerate(_LI_TEMPLATES, 1):
        text = tpl.format(word=ocr_word)
        test_id = f"li_{correct_word}_t{tidx}"
        CHAR_LI_CASES.append((text, ocr_word, correct_word, test_id))


# ── 1e. fi  ligature garble  (20 words × 5 = 100 tests) ─────────────

_FI_WORDS = [
    ("fmd", "find"),
    ("ftre", "fire"),
    ("ftsh", "fish"),
    ("ftll", "fill"),
    ("ftlm", "film"),
    ("ftnal", "final"),
    ("ftnance", "finance"),
    ("ftnger", "finger"),
    ("ftmsh", "finish"),
    ("ftrm", "firm"),
    ("ftrst", "first"),
    ("ftve", "five"),
    ("fteld", "field"),
    ("ftght", "fight"),
    ("ftgure", "figure"),
    ("ftle", "file"),
    ("ftlter", "filter"),
    ("ftne", "fine"),
    ("fttness", "fitness"),
    ("ftxed", "fixed"),
]

_FI_TEMPLATES = [
    "The team managed to {word} the correct answer quickly",
    "Officials agreed to {word} the ongoing investigation",
    "The report failed to {word} any significant improvements",
    "Researchers hoped to {word} new evidence in the study",
    "The committee planned to {word} the budget before year end",
]

CHAR_FI_CASES = []
for ocr_word, correct_word in _FI_WORDS:
    for tidx, tpl in enumerate(_FI_TEMPLATES, 1):
        text = tpl.format(word=ocr_word)
        test_id = f"fi_{correct_word}_t{tidx}"
        CHAR_FI_CASES.append((text, ocr_word, correct_word, test_id))


# ── 1f. m → rn  and other confusions  (30 words × 5 = 150 tests) ─────

_MISC_CONF_WORDS = [
    ("hurnan", "human"),
    ("burrn", "burn"),
    ("warrn", "warm"),
    ("harrn", "harm"),
    ("alarrn", "alarm"),
    ("charrn", "charm"),
    ("farrn", "farm"),
    ("storrn", "storm"),
    ("reforrn", "reform"),
    ("platforrn", "platform"),
    ("uniforrn", "uniform"),
    ("transforrn", "transform"),
    ("perforrn", "perform"),
    ("inforrn", "inform"),
    ("confrrn", "confirm"),
    ("affrrn", "affirm"),
    ("worrn", "worm"),
    ("norrn", "norm"),
    ("forrn", "form"),
    ("borrn", "born"),
    ("corrn", "corn"),
    ("horrn", "horn"),
    ("torrn", "torn"),
    ("learrn", "learn"),
    ("earrn", "earn"),
    ("turrn", "turn"),
    ("returrn", "return"),
    ("concerrn", "concern"),
    ("patterrn", "pattern"),
    ("moderrn", "modern"),
]

_MISC_CONF_TEMPLATES = [
    "The organization decided to {word} its existing approach",
    "The {word} was featured in the quarterly progress report",
    "Local authorities examined the {word} for regulatory compliance",
    "The {word} underwent extensive testing before deployment",
    "Stakeholders expressed confidence in the proposed {word}",
]

CHAR_MISC_CASES = []
for ocr_word, correct_word in _MISC_CONF_WORDS:
    for tidx, tpl in enumerate(_MISC_CONF_TEMPLATES, 1):
        text = tpl.format(word=ocr_word)
        test_id = f"misc_{correct_word}_t{tidx}"
        CHAR_MISC_CASES.append((text, ocr_word, correct_word, test_id))


# Combine all character-confusion cases
CHAR_CONFUSION_CASES = (
    CHAR_RN_M_CASES
    + CHAR_CL_D_CASES
    + CHAR_VV_W_CASES
    + CHAR_LI_CASES
    + CHAR_FI_CASES
    + CHAR_MISC_CASES
)


@pytest.mark.integration
@pytest.mark.ocr_positive
@pytest.mark.parametrize(
    "text,error_word,expected_correction,test_id", CHAR_CONFUSION_CASES
)
def test_ocr_char_confusion(text, error_word, expected_correction, test_id, api):
    body = ocr_check(api, text)
    assert body["result"] == "issue_detected", (
        f"[{test_id}] Should detect '{error_word}'"
    )
    span_texts = {s["text"] for s in body.get("spans", [])}
    assert error_word in span_texts, (
        f"[{test_id}] Missing span for '{error_word}'"
    )
    if expected_correction:
        span = next(s for s in body["spans"] if s["text"] == error_word)
        sugg_texts = {s["text"].lower() for s in span.get("suggestions", [])}
        assert expected_correction.lower() in sugg_texts, (
            f"[{test_id}] Missing correction '{expected_correction}'"
        )


# ═══════════════════════════════════════════════════════════════════════
# 2. TRANSPOSITIONS  (60 words × 10 templates = 600 tests)
# ═══════════════════════════════════════════════════════════════════════

_TRANSPOSITION_WORDS = [
    ("teh", "the"),
    ("taht", "that"),
    ("tihs", "this"),
    ("wiht", "with"),
    ("hvae", "have"),
    ("tehy", "they"),
    ("bene", "been"),
    ("thier", "their"),
    ("abuot", "about"),
    ("woudl", "would"),
    ("tehre", "there"),
    ("whcih", "which"),
    ("coudl", "could"),
    ("ohter", "other"),
    ("aftre", "after"),
    ("thsoe", "those"),
    ("wehre", "where"),
    ("shoudl", "should"),
    ("mihgt", "might"),
    ("bieng", "being"),
    ("nevre", "never"),
    ("eevry", "every"),
    ("sicne", "since"),
    ("thougth", "thought"),
    ("thoguh", "though"),
    ("betwene", "between"),
    ("agaisnt", "against"),
    ("durign", "during"),
    ("beofre", "before"),
    ("wihtout", "without"),
    ("anohter", "another"),
    ("becuase", "because"),
    ("aruond", "around"),
    ("togehter", "together"),
    ("alraedy", "already"),
    ("enoguh", "enough"),
    ("beleive", "believe"),
    ("perhpas", "perhaps"),
    ("oftem", "often"),
    ("abvoe", "above"),
    ("whlie", "while"),
    ("amnog", "among"),
    ("untli", "until"),
    ("sitll", "still"),
    ("alawys", "always"),
    ("ealry", "early"),
    ("rahter", "rather"),
    ("whsoe", "whose"),
    ("qutie", "quite"),
    ("ligth", "light"),
    ("huamn", "human"),
    ("womain", "woman"),
    ("watre", "water"),
    ("paepr", "paper"),
    ("maojr", "major"),
    ("bagen", "began"),
    ("sceince", "science"),
    ("poilcy", "policy"),
    ("reprot", "report"),
    ("chagne", "change"),
]

_TRANSPOSITION_TEMPLATES = [
    "Investigators confirmed {word} the document was submitted to the review board",
    "The committee found {word} the evidence was compelling",
    "Everyone acknowledged {word} the results were significant",
    "Records show {word} the decision was made unanimously",
    "The analysis confirmed {word} the data supported the claim",
    "It became clear {word} the project needed more resources",
    "The witness stated {word} the incident occurred at noon",
    "Officials determined {word} the procedure was followed",
    "The investigation revealed {word} the original plan had flaws",
    "Experts concluded {word} the approach was fundamentally sound",
]

TRANSPOSITION_CASES = []
for ocr_word, correct_word in _TRANSPOSITION_WORDS:
    for tidx, tpl in enumerate(_TRANSPOSITION_TEMPLATES, 1):
        text = tpl.format(word=ocr_word)
        test_id = f"trans_{correct_word}_t{tidx}"
        TRANSPOSITION_CASES.append((text, ocr_word, correct_word, test_id))


@pytest.mark.integration
@pytest.mark.ocr_positive
@pytest.mark.parametrize(
    "text,error_word,expected_correction,test_id", TRANSPOSITION_CASES
)
def test_ocr_transposition(text, error_word, expected_correction, test_id, api):
    body = ocr_check(api, text)
    assert body["result"] == "issue_detected", (
        f"[{test_id}] Should detect '{error_word}'"
    )
    span_texts = {s["text"] for s in body.get("spans", [])}
    assert error_word in span_texts, (
        f"[{test_id}] Missing span for '{error_word}'"
    )
    if expected_correction:
        span = next(s for s in body["spans"] if s["text"] == error_word)
        sugg_texts = {s["text"].lower() for s in span.get("suggestions", [])}
        assert expected_correction.lower() in sugg_texts, (
            f"[{test_id}] Missing correction '{expected_correction}'"
        )


# ═══════════════════════════════════════════════════════════════════════
# 3. MULTIPLE ERRORS PER TEXT  (400 tests)
#    100 base sentences × 4 corruption variants
# ═══════════════════════════════════════════════════════════════════════

MULTI_ERROR_CASES = [
    # ── base 1 ──
    ("The g0vernment p0licy was reviewed by the cornrnittee", 2, "multi_1a"),
    ("The governrnent p0licy was revievved by the committee", 2, "multi_1b"),
    ("The g0vernment poIicy was reviewed by teh committee", 2, "multi_1c"),
    ("The governrnent poIicy was revievved by teh cornrnittee", 3, "multi_1d"),
    # ── base 2 ──
    ("Teh departrment issued a new p0licy docurnent", 2, "multi_2a"),
    ("The departrment issuecl a nevv p0licy document", 2, "multi_2b"),
    ("Teh department issued a nevv poIicy docurnent", 2, "multi_2c"),
    ("Teh departrment issued a nevv p0licy docurnent", 3, "multi_2d"),
    # ── base 3 ──
    ("The environrnent needs irnrnediate pr0tection from p0llution", 2, "multi_3a"),
    ("Teh environment needs immediate protecti0n frorn pollution", 2, "multi_3b"),
    ("The environrnent needs irnrnediate protecti0n from pollution", 2, "multi_3c"),
    ("Teh environrnent needs irnrnediate pr0tection frorn p0llution", 3, "multi_3d"),
    # ── base 4 ──
    ("Citizens shoudl exarnine the 0fficial rep0rt carefully", 2, "multi_4a"),
    ("Citizens should exarnine teh officiaI report carefuIIy", 2, "multi_4b"),
    ("Citizens shoudl examine the officiaI rep0rt carefuIIy", 2, "multi_4c"),
    ("Citizens shoudl exarnine teh 0fficial rep0rt carefuIIy", 3, "multi_4d"),
    # ── base 5 ──
    ("The developrnent of the cornrnunity was a rnajor priority", 2, "multi_5a"),
    ("Teh development of the cornrnunity was a major pri0rity", 2, "multi_5b"),
    ("The developrnent of teh community vvas a major priority", 2, "multi_5c"),
    ("Teh developrnent of the cornrnunity vvas a rnajor pri0rity", 3, "multi_5d"),
    # ── base 6 ──
    ("The 0rganization pubiished its annuaI rep0rt yesterday", 2, "multi_6a"),
    ("Teh organization pubIished its annual rep0rt yesterday", 2, "multi_6b"),
    ("The organizati0n pubiished its annuaI report yesterclay", 2, "multi_6c"),
    ("Teh 0rganization pubIished its annuaI rep0rt yesterclay", 3, "multi_6d"),
    # ── base 7 ──
    ("Researchers condudecl that the experirnent was a success", 2, "multi_7a"),
    ("Researchers concluded taht the experirnent vvas a success", 2, "multi_7b"),
    ("Researchers condudecl taht the experiment was a succ3ss", 2, "multi_7c"),
    ("Researchers condudecl taht the experirnent vvas a succ3ss", 3, "multi_7d"),
    # ── base 8 ──
    ("Teh cornrnercial district was transforrned over the decade", 2, "multi_8a"),
    ("The cornrnercial district vvas transformed over the clecade", 2, "multi_8b"),
    ("Teh commercial clistrict was transforrned over the decade", 2, "multi_8c"),
    ("Teh cornrnercial clistrict vvas transforrned over the clecade", 3, "multi_8d"),
    # ── base 9 ──
    ("The tourrnarment attracted thousands of sp3ctators", 2, "multi_9a"),
    ("Teh tournament attracted thous4nds of spectators", 2, "multi_9b"),
    ("The tourrnarment attractecl thousands 0f spectators", 2, "multi_9c"),
    ("Teh tourrnarment attractecl thous4nds 0f sp3ctators", 3, "multi_9d"),
    # ── base 10 ──
    ("Iocel authorities confirmed the perrnanent closure", 2, "multi_10a"),
    ("Local auth0rities confirrned the perrnanent closure", 2, "multi_10b"),
    ("IocaI authorities confirrned teh permanent cIosure", 2, "multi_10c"),
    ("IocaI auth0rities confirrned the perrnanent cIosure", 3, "multi_10d"),
    # ── base 11 ──
    ("The ftnal report indudecl several recornrnendations", 2, "multi_11a"),
    ("Teh final rep0rt included several recornrnendations", 2, "multi_11b"),
    ("The ftnal report incIuded severaI recommendations", 2, "multi_11c"),
    ("Teh ftnal rep0rt indudecl severaI recornrnendations", 3, "multi_11d"),
    # ── base 12 ──
    ("The instrurnent was usecl for rneasuring ternperature", 2, "multi_12a"),
    ("Teh instrument vvas used for measuring ternperature", 2, "multi_12b"),
    ("The instrurnent was used f0r measuring temperature", 2, "multi_12c"),
    ("Teh instrurnent vvas usecl f0r rneasuring ternperature", 3, "multi_12d"),
    # ── base 13 ──
    ("Teh cornrnittee examinecl the proposed arnendment", 2, "multi_13a"),
    ("The cornrnittee examined teh proposed arnendrnent", 2, "multi_13b"),
    ("Teh committee exarnined the prop0sed amendment", 2, "multi_13c"),
    ("Teh cornrnittee examinecl the prop0sed arnendrnent", 3, "multi_13d"),
    # ── base 14 ──
    ("Teh governrnent announced a fundarnental reforrn plan", 2, "multi_14a"),
    ("The governrnent announcecl a fundamental reforrn plan", 2, "multi_14b"),
    ("Teh government announced a fundarnental reform pIan", 2, "multi_14c"),
    ("Teh governrnent announcecl a fundarnental reforrn pIan", 3, "multi_14d"),
    # ── base 15 ──
    ("The experirnental platforrn was deployecl last rnonth", 2, "multi_15a"),
    ("Teh experimental platform vvas deployed Iast month", 2, "multi_15b"),
    ("The experirnental pIatform was deployed last rnonth", 2, "multi_15c"),
    ("Teh experirnental platforrn vvas deployecl Iast rnonth", 3, "multi_15d"),
    # ── base 16 ──
    ("Students shoudl cornplete the assignrnent by Friday", 2, "multi_16a"),
    ("Stuclents should complete the assignrnent by Friclay", 2, "multi_16b"),
    ("Students shoudl complete teh assignment by Friday", 2, "multi_16c"),
    ("Stuclents shoudl cornplete the assignrnent by Friclay", 3, "multi_16d"),
    # ── base 17 ──
    ("The p0lice departrment annouced new safety rneasures", 2, "multi_17a"),
    ("Teh police department announced nevv safety measures", 2, "multi_17b"),
    ("The poIice departrment announced new safety rneasures", 2, "multi_17c"),
    ("Teh p0lice departrment annouced nevv safety rneasures", 3, "multi_17d"),
    # ── base 18 ──
    ("The nurnerical analysis producecl unexpected results", 2, "multi_18a"),
    ("Teh numerical anaIysis produced unexpected resuIts", 2, "multi_18b"),
    ("The nurnerical anaIysis producecl unexpected results", 2, "multi_18c"),
    ("Teh nurnerical anaIysis producecl unexpected resuIts", 3, "multi_18d"),
    # ── base 19 ──
    ("Residents dernanded irnrnediate action frorn the council", 2, "multi_19a"),
    ("Residents demanded irnrnediate acti0n from the counciI", 2, "multi_19b"),
    ("Residents dernanded immediate action frorn teh council", 2, "multi_19c"),
    ("Residents dernanded irnrnediate acti0n frorn teh counciI", 3, "multi_19d"),
    # ── base 20 ──
    ("The articde described the spectadular transforrnnation", 2, "multi_20a"),
    ("Teh article described the spectadular transformation", 2, "multi_20b"),
    ("The artide clescribed the spectacular transforrnnation", 2, "multi_20c"),
    ("Teh articde clescribed the spectadular transforrnnation", 3, "multi_20d"),
    # ── base 21 ──
    ("The crirninal was apprehendecl near the tovvn center", 2, "multi_21a"),
    ("Teh criminal was apprehended near the tovvn center", 2, "multi_21b"),
    ("The crirninal vvas apprehended near the town center", 2, "multi_21c"),
    ("Teh crirninal vvas apprehendecl near the tovvn center", 3, "multi_21d"),
    # ── base 22 ──
    ("The rnedical facility requirecl additional equiprnent", 2, "multi_22a"),
    ("Teh medical faciIity required additionaI equipment", 2, "multi_22b"),
    ("The rnedical facility required additi0nal equipment", 2, "multi_22c"),
    ("Teh rnedical faciIity requirecl additi0nal equiprnent", 3, "multi_22d"),
    # ── base 23 ──
    ("Parents shoudl rnonitor thier children's activities", 2, "multi_23a"),
    ("Parents shouId monitor their chiIdren's activities", 2, "multi_23b"),
    ("Parents shoudl monitor their chiIdren's activiti3s", 2, "multi_23c"),
    ("Parents shoudl rnonitor thier chiIdren's activiti3s", 3, "multi_23d"),
    # ── base 24 ──
    ("The terrninal was closecl for rnaintenance last week", 2, "multi_24a"),
    ("Teh terminal was closed for rnaintenance Iast week", 2, "multi_24b"),
    ("The terrninal vvas closed for maintenance last vveek", 2, "multi_24c"),
    ("Teh terrninal vvas closecl for rnaintenance Iast vveek", 3, "multi_24d"),
    # ── base 25 ──
    ("The vehicde's perrnanent registration was approvecl", 2, "multi_25a"),
    ("Teh vehicle's permanent registrati0n was approved", 2, "multi_25b"),
    ("The vehicde's perrnanent registrati0n was approved", 2, "multi_25c"),
    ("Teh vehicde's perrnanent registrati0n vvas approvecl", 3, "multi_25d"),
    # ── base 26 ──
    ("Teh comrnission released a prelimirary rep0rt today", 2, "multi_26a"),
    ("The cornrnission released a prelirninary report toclay", 2, "multi_26b"),
    ("Teh commission reIeased a preliminary rep0rt today", 2, "multi_26c"),
    ("Teh cornrnission reIeased a prelirninary rep0rt toclay", 3, "multi_26d"),
    # ── base 27 ──
    ("Teh moledular structure was analyzecl in the Iab", 2, "multi_27a"),
    ("The moledular structure vvas analyzed in the lab", 2, "multi_27b"),
    ("Teh molecular structure was anaIyzed in the Iab", 2, "multi_27c"),
    ("Teh moledular structure vvas analyzecl in the Iab", 3, "multi_27d"),
    # ── base 28 ──
    ("The rnineral deposits were discoveredl Iast year", 2, "multi_28a"),
    ("Teh mineral dep0sits were discovered last year", 2, "multi_28b"),
    ("The rnineral deposits vvere discovered last year", 2, "multi_28c"),
    ("Teh rnineral dep0sits vvere discoveredl Iast year", 3, "multi_28d"),
    # ── base 29 ──
    ("Workers dernanded that the uniforrn policy be changed", 2, "multi_29a"),
    ("Vvorkers demanded that the uniforrn poIicy be changed", 2, "multi_29b"),
    ("Workers dernanded that the uniform p0licy be changecl", 2, "multi_29c"),
    ("Vvorkers dernanded that the uniforrn p0licy be changecl", 3, "multi_29d"),
    # ── base 30 ──
    ("The alarnm system was testecl during the storm", 2, "multi_30a"),
    ("Teh alarm systern was tested durign the storm", 2, "multi_30b"),
    ("The alarrn system vvas tested during the storrn", 2, "multi_30c"),
    ("Teh alarrn systern vvas testecl durign the storrn", 3, "multi_30d"),
    # ── base 31 ──
    ("The platforrn supportecl thousands of daily users", 2, "multi_31a"),
    ("Teh platform supp0rted thousands of daily users", 2, "multi_31b"),
    ("The platforrn supported thous4nds of daiIy users", 2, "multi_31c"),
    ("Teh platforrn supp0rted thous4nds of daiIy users", 3, "multi_31d"),
    # ── base 32 ──
    ("The rnuseum displayed a spectadular coIlection", 2, "multi_32a"),
    ("Teh museum dispIayed a spectacular collection", 2, "multi_32b"),
    ("The rnuseum dispIayed a spectadular collection", 2, "multi_32c"),
    ("Teh rnuseum dispIayed a spectadular coIlection", 3, "multi_32d"),
    # ── base 33 ──
    ("Participants shoudl cornplete the registration forrn", 2, "multi_33a"),
    ("Participants shouId complete teh registration form", 2, "multi_33b"),
    ("Participants shoudl compIete the registrati0n form", 2, "multi_33c"),
    ("Participants shoudl cornplete teh registrati0n forrn", 3, "multi_33d"),
    # ── base 34 ──
    ("The educati0n systern needs fundarnental changes", 2, "multi_34a"),
    ("Teh education system needs fundarnental changecl", 2, "multi_34b"),  # noqa: E501
    ("The educati0n systern needs fundamental changecl", 2, "multi_34c"),
    ("Teh educati0n systern needs fundarnental changecl", 3, "multi_34d"),
    # ── base 35 ──
    ("The recornrnendation was acceptecl by the board", 2, "multi_35a"),
    ("Teh recommendation vvas accepted by the board", 2, "multi_35b"),
    ("The recornrnendation was accepted by teh board", 2, "multi_35c"),
    ("Teh recornrnendation vvas acceptecl by teh board", 3, "multi_35d"),
    # ── base 36 ──
    ("International cornrnunication irnproved significantIy", 2, "multi_36a"),
    ("InternationaI communication improved significantIy", 2, "multi_36b"),
    ("Internati0nal cornrnunication improved significantly", 2, "multi_36c"),
    ("Internati0nal cornrnunication irnproved significantIy", 3, "multi_36d"),
    # ── base 37 ──
    ("The rnernorial was visitecl by thousands of tourists", 2, "multi_37a"),
    ("Teh memorial vvas visited by thousands of tourists", 2, "multi_37b"),
    ("The rnernorial was visited by thous4nds of tourists", 2, "multi_37c"),
    ("Teh rnernorial vvas visitecl by thous4nds of tourists", 3, "multi_37d"),
    # ── base 38 ──
    ("The ftnancial report indudecl quarterly earnings", 2, "multi_38a"),
    ("Teh financial rep0rt included quarterly earnings", 2, "multi_38b"),
    ("The ftnancial report incIuded quarterIy earnings", 2, "multi_38c"),
    ("Teh ftnancial rep0rt indudecl quarterIy earnings", 3, "multi_38d"),
    # ── base 39 ──
    ("The nationaI parkl attracted rnillions of visitors", 2, "multi_39a"),
    ("Teh national park attracted miIIions of visitors", 2, "multi_39b"),
    ("The nationaI park attractecl millions of visit0rs", 2, "multi_39c"),
    ("Teh nationaI parkl attractecl rnillions of visit0rs", 3, "multi_39d"),
    # ── base 40 ──
    ("Scientists perforrned experirnents in the laboratory", 2, "multi_40a"),
    ("Teh scientists performed experirnents in the Iab", 2, "multi_40b"),
    ("Scientists perforrned experiments in teh laboratory", 2, "multi_40c"),
    ("Teh scientists perforrned experirnents in teh Iaboratory", 3, "multi_40d"),
    # ── base 41 ──
    ("The cornrnunity center hostecl a fundraising event", 2, "multi_41a"),
    ("Teh community center hosted a fundraising ev3nt", 2, "multi_41b"),
    ("The cornrnunity center hosted a funclraising event", 2, "multi_41c"),
    ("Teh cornrnunity center hostecl a funclraising ev3nt", 3, "multi_41d"),
    # ── base 42 ──
    ("The therrrnal energy systern was highly efficient", 2, "multi_42a"),
    ("Teh thermal energy system vvas highIy efficient", 2, "multi_42b"),
    ("The therrrnal energy systern was highIy efficient", 2, "multi_42c"),
    ("Teh therrrnal energy systern vvas highIy efficient", 3, "multi_42d"),
    # ── base 43 ──
    ("Management approvecl the budg3t for the new project", 2, "multi_43a"),
    ("Managernent approved teh budget for the nevv project", 2, "multi_43b"),
    ("Management approvecl the budget for teh nevv project", 2, "multi_43c"),
    ("Managernent approvecl the budg3t for teh nevv project", 3, "multi_43d"),
    # ── base 44 ──
    ("Teh teacher explalined the experirnental procedure", 2, "multi_44a"),
    ("The teacher expIained the experirnental procedure", 2, "multi_44b"),
    ("Teh teacher explalined the experimental procedur3", 2, "multi_44c"),
    ("Teh teacher expIained the experirnental procedur3", 3, "multi_44d"),
    # ── base 45 ──
    ("The sedular instituti0n published new guideIines", 2, "multi_45a"),
    ("Teh secular institution pubIished new guidelines", 2, "multi_45b"),
    ("The sedular institution published nevv guidelines", 2, "multi_45c"),
    ("Teh sedular instituti0n pubIished nevv guideIines", 3, "multi_45d"),
    # ── base 46 ──
    ("Teh rnanager confirrned the schedule for the event", 2, "multi_46a"),
    ("The rnanager confirmed teh schedule for the ev3nt", 2, "multi_46b"),
    ("Teh manager confirrned the scheduIe for the event", 2, "multi_46c"),
    ("Teh rnanager confirrned teh scheduIe for the ev3nt", 3, "multi_46d"),
    # ── base 47 ──
    ("The hospitaI adminlstration announcecl new policies", 2, "multi_47a"),
    ("Teh hospital administration announced nevv poIicies", 2, "multi_47b"),
    ("The hospitaI administration announced nevv policies", 2, "multi_47c"),
    ("Teh hospitaI adminlstration announcecl nevv poIicies", 3, "multi_47d"),
    # ── base 48 ──
    ("Voters shoudl exarnine eachl candidate's platform", 2, "multi_48a"),
    ("V0ters should examine each canclidate's platform", 2, "multi_48b"),
    ("Voters shoudl exarnine each candidate's pIatform", 2, "multi_48c"),
    ("V0ters shoudl exarnine eachl canclidate's pIatform", 3, "multi_48d"),
    # ── base 49 ──
    ("The docurnent was signecl by all participating parties", 2, "multi_49a"),
    ("Teh document vvas signed by all participating parties", 2, "multi_49b"),
    ("The docurnent was signed by aII participating parti3s", 2, "multi_49c"),
    ("Teh docurnent vvas signecl by aII participating parti3s", 3, "multi_49d"),
    # ── base 50 ──
    ("The anirnai shelter receivecl generous donations", 2, "multi_50a"),
    ("Teh animal sheIter received gen3rous donations", 2, "multi_50b"),
    ("The anirnai sheIter received generous donations", 2, "multi_50c"),
    ("Teh anirnai sheIter receivecl gen3rous donations", 3, "multi_50d"),
    # ── base 51 ──
    ("The rnilitary cornrnander issuecl new orders today", 2, "multi_51a"),
    ("Teh military commander issued nevv 0rders today", 2, "multi_51b"),
    ("The rnilitary commander issued new orclers today", 2, "multi_51c"),
    ("Teh rnilitary cornrnander issuecl nevv orclers today", 3, "multi_51d"),
    # ── base 52 ──
    ("The ftlm festival attractecl international attention", 2, "multi_52a"),
    ("Teh film festivaI attracted internationaI attention", 2, "multi_52b"),
    ("The ftlm festivaI attracted international attenti0n", 2, "multi_52c"),
    ("Teh ftlm festivaI attractecl internationaI attenti0n", 3, "multi_52d"),
    # ── base 53 ──
    ("The irnportant docurnent was filed vvith the court", 2, "multi_53a"),
    ("Teh important document was fiIed with the c0urt", 2, "multi_53b"),
    ("The irnportant document was fiIed with the court", 2, "multi_53c"),
    ("Teh irnportant docurnent was fiIed vvith the c0urt", 3, "multi_53d"),
    # ── base 54 ──
    ("Traffic congesti0n increasecl during the surnrner months", 2, "multi_54a"),
    ("Teh traffic congestion increased during the surnrner months", 2, "multi_54b"),
    ("Traffic congesti0n increased durign the summer months", 2, "multi_54c"),
    ("Teh traffic congesti0n increasecl durign the surnrner months", 3, "multi_54d"),
    # ── base 55 ──
    ("The netvvork systern requirecl significant upgrades", 2, "multi_55a"),
    ("Teh network system required signific4nt upgrades", 2, "multi_55b"),
    ("The netvvork systern required significant upgracles", 2, "multi_55c"),
    ("Teh netvvork systern requirecl signific4nt upgracles", 3, "multi_55d"),
    # ── base 56 ──
    ("The corrununity gardlen provided fresh vegetables", 2, "multi_56a"),
    ("Teh community garden provicled fresh vegetabIes", 2, "multi_56b"),
    ("The corrununity garden proviclecl fresh vegetables", 2, "multi_56c"),
    ("Teh corrununity gardlen provicled fresh vegetabIes", 3, "multi_56d"),
    # ── base 57 ──
    ("Engineers redesignecl the therrnal protection systern", 2, "multi_57a"),
    ("Teh engineers redesigned the thermaI protection system", 2, "multi_57b"),
    ("Engineers redesignecl the thermal protecti0n system", 2, "multi_57c"),
    ("Teh engineers redesignecl the therrnal protecti0n systern", 3, "multi_57d"),
    # ── base 58 ──
    ("The rnedical tearn completed teh surgical procedure", 2, "multi_58a"),
    ("The rnedical team cornpleted the surgical procedure", 2, "multi_58b"),
    ("Teh medical tearn completed the surgicaI procedure", 2, "multi_58c"),
    ("Teh rnedical tearn cornpleted the surgicaI procedure", 3, "multi_58d"),
    # ── base 59 ──
    ("Investigators reviewecl the crirninal's background", 2, "multi_59a"),
    ("Teh investigators reviewed the criminaI's backgr0und", 2, "multi_59b"),
    ("Investigators reviewecl the criminal's backgrounld", 2, "multi_59c"),
    ("Teh investigators reviewecl the crirninal's backgr0und", 3, "multi_59d"),
    # ── base 60 ──
    ("The schooi district approvecl a new curriculurn", 2, "multi_60a"),
    ("Teh school district approved a nevv curriculum", 2, "multi_60b"),
    ("The schooi district approved a new curricuIum", 2, "multi_60c"),
    ("Teh schooi district approvecl a nevv curricuIurn", 3, "multi_60d"),
    # ── base 61 ──
    ("The pubIic Iibrary expanded its digitaI collection", 2, "multi_61a"),
    ("Teh public Iibrary expanded its digital coIIection", 2, "multi_61b"),
    ("The pubIic library expandecl its digital collection", 2, "multi_61c"),
    ("Teh pubIic Iibrary expandecl its digitaI coIIection", 3, "multi_61d"),
    # ── base 62 ──
    ("The transportati0n systern servecl millions of riders", 2, "multi_62a"),
    ("Teh transportation system served miIIions of riders", 2, "multi_62b"),
    ("The transportati0n system served millions 0f riders", 2, "multi_62c"),
    ("Teh transportati0n systern servecl miIIions 0f riders", 3, "multi_62d"),
    # ── base 63 ──
    ("Teh construction cornpany completed the tovver on tirne", 2, "multi_63a"),
    ("The construction cornpany cornpleted the tower on time", 2, "multi_63b"),
    ("Teh construction company completed the tovver 0n time", 2, "multi_63c"),
    ("Teh construction cornpany cornpleted the tovver on tirne", 3, "multi_63d"),
    # ── base 64 ──
    ("The forrrnal investigation uncoverecl critical evidence", 2, "multi_64a"),
    ("Teh formal investigati0n uncovered critical evidence", 2, "multi_64b"),
    ("The forrrnal investigation uncovered criticaI evid3nce", 2, "multi_64c"),
    ("Teh forrrnal investigati0n uncoverecl criticaI evid3nce", 3, "multi_64d"),
    # ── base 65 ──
    ("Several ernployees cornplained about the new policy", 2, "multi_65a"),
    ("SeveraI employees compIained about teh new policy", 2, "multi_65b"),
    ("Several ernployees complained abuot the nevv policy", 2, "multi_65c"),
    ("SeveraI ernployees cornplained abuot teh nevv policy", 3, "multi_65d"),
    # ── base 66 ──
    ("Teh judge dismissecl the case due to insufficient evidence", 2, "multi_66a"),
    ("The juclge dismissed teh case due to insufficient evicl3nce", 2, "multi_66b"),
    ("Teh judge dismissed the cas3 due to insufficient evidence", 2, "multi_66c"),
    ("Teh juclge dismissecl teh cas3 due to insufficient evicl3nce", 3, "multi_66d"),
    # ── base 67 ──
    ("The vvindow was brokecl during the severe storm", 2, "multi_67a"),
    ("Teh window vvas broken during the severe storrn", 2, "multi_67b"),
    ("The vvindow was broken durign the severe storm", 2, "multi_67c"),
    ("Teh vvindow vvas brokecl durign the severe storrn", 3, "multi_67d"),
    # ── base 68 ──
    ("The cornpany's annuaI revenue increasecl significantly", 2, "multi_68a"),
    ("Teh company's annual revenue incr3ased significantly", 2, "multi_68b"),
    ("The cornpany's annual revenu3 increased significantIy", 2, "multi_68c"),
    ("Teh cornpany's annuaI revenu3 increasecl significantIy", 3, "multi_68d"),
    # ── base 69 ──
    ("The rnusician perforrned a beautifuI concert last night", 2, "multi_69a"),
    ("Teh musician performed a beautiful conc3rt last night", 2, "multi_69b"),
    ("The rnusician performed a beautiful conc3rt Iast night", 2, "multi_69c"),
    ("Teh rnusician perforrned a beautifuI conc3rt Iast night", 3, "multi_69d"),
    # ── base 70 ──
    ("Teh archit3ct designed a spectadular building", 2, "multi_70a"),
    ("The architect clesigned a spectadular buiIding", 2, "multi_70b"),
    ("Teh architect designed a spectacular buiIding", 2, "multi_70c"),
    ("Teh archit3ct clesigned a spectadular buiIding", 3, "multi_70d"),
    # ── base 71 ──
    ("The presid3nt announcecl a new trade agreernent", 2, "multi_71a"),
    ("Teh president announced a nevv trade agreement", 2, "multi_71b"),
    ("The presid3nt announced a new trade agreernent", 2, "multi_71c"),
    ("Teh presid3nt announcecl a nevv trade agreernent", 3, "multi_71d"),
    # ── base 72 ──
    ("Teh university publishecl its research ftndings", 2, "multi_72a"),
    ("The university pubIished its research findings", 2, "multi_72b"),
    ("Teh university published its res3arch findings", 2, "multi_72c"),
    ("Teh university publishecl its res3arch ftndings", 3, "multi_72d"),
    # ── base 73 ──
    ("The environmentaI agency rnonitored the watre quality", 2, "multi_73a"),
    ("Teh environmental ag3ncy monitored the water quality", 2, "multi_73b"),
    ("The environmentaI agency monitored teh water quaIity", 2, "multi_73c"),
    ("Teh environmentaI ag3ncy rnonitored the watre quaIity", 3, "multi_73d"),
    # ── base 74 ──
    ("Teh software developrnent tearn released a new version", 2, "multi_74a"),
    ("The software developrnent team reIeased a nevv version", 2, "multi_74b"),
    ("Teh software development tearn released a new versi0n", 2, "multi_74c"),
    ("Teh software developrnent tearn reIeased a nevv versi0n", 3, "multi_74d"),
    # ── base 75 ──
    ("The farrner harvested a rnajor crop this season", 2, "multi_75a"),
    ("Teh farmer harvested a major cr0p this season", 2, "multi_75b"),
    ("The farrner harvested a major cr0p this seas0n", 2, "multi_75c"),
    ("Teh farrner harvested a rnajor cr0p this seas0n", 3, "multi_75d"),
    # ── base 76 ──
    ("The factory producecl thousands of uniforrns daily", 2, "multi_76a"),
    ("Teh factory produced thous4nds of uniforms daily", 2, "multi_76b"),
    ("The factory producecl thous4nds of uniforms daiIy", 2, "multi_76c"),
    ("Teh factory producecl thous4nds of uniforrns daiIy", 3, "multi_76d"),
    # ── base 77 ──
    ("The historian exarnined ancierit docurnents carefully", 2, "multi_77a"),
    ("Teh historian examined ancient docurnents carefuIIy", 2, "multi_77b"),
    ("The historian exarnined ancient documents carefuIIy", 2, "multi_77c"),
    ("Teh historian exarnined ancierit docurnents carefuIIy", 3, "multi_77d"),
    # ── base 78 ──
    ("Teh clirnate scientists publishecl their findings", 2, "multi_78a"),
    ("The climate sci3ntists published their ftndings", 2, "multi_78b"),
    ("Teh climate scientists published thier findings", 2, "multi_78c"),
    ("Teh clirnate sci3ntists publishecl thier ftndings", 3, "multi_78d"),
    # ── base 79 ──
    ("The dernonstration attractecl international rnedia attention", 2, "multi_79a"),
    ("Teh demonstration attracted internationaI media attenti0n", 2, "multi_79b"),
    ("The dernonstration attracted international rnedia attenti0n", 2, "multi_79c"),
    ("Teh dernonstration attractecl internationaI rnedia attenti0n", 3, "multi_79d"),
    # ── base 80 ──
    ("Engineers testecl the netvvork security protoc0l", 2, "multi_80a"),
    ("Teh engineers tested the network security protocoI", 2, "multi_80b"),
    ("Engineers testecl the network s3curity protocol", 2, "multi_80c"),
    ("Teh engineers testecl the netvvork s3curity protoc0l", 3, "multi_80d"),
    # ── base 81 ──
    ("The hospit4l announcecl new visiting hours", 2, "multi_81a"),
    ("Teh hospital announced nevv visiting h0urs", 2, "multi_81b"),
    ("The hospit4l announced new visiting h0urs", 2, "multi_81c"),
    ("Teh hospit4l announcecl nevv visiting h0urs", 3, "multi_81d"),
    # ── base 82 ──
    ("The experirnental rnedicine showed prornising results", 2, "multi_82a"),
    ("Teh experimental medicine shovved promising resuIts", 2, "multi_82b"),
    ("The experirnental medicine showed prornising resuIts", 2, "multi_82c"),
    ("Teh experirnental rnedicine shovved prornising resuIts", 3, "multi_82d"),
    # ── base 83 ──
    ("The Iibrary catalogl contained rnillions of entries", 2, "multi_83a"),
    ("Teh library catalog contained miIIions of entri3s", 2, "multi_83b"),
    ("The Iibrary catalog containecl millions of entries", 2, "multi_83c"),
    ("Teh Iibrary catalogl containecl rnillions of entri3s", 3, "multi_83d"),
    # ── base 84 ──
    ("The technol0gy cornpany announcecl a merger", 2, "multi_84a"),
    ("Teh technology company announced a rnerg3r", 2, "multi_84b"),
    ("The technol0gy company announced a rnerg3r", 2, "multi_84c"),
    ("Teh technol0gy cornpany announcecl a rnerg3r", 3, "multi_84d"),
    # ── base 85 ──
    ("Teh volunteer organizati0n helped thousands of farnilies", 2, "multi_85a"),
    ("The voIunteer organization heIped thousands of families", 2, "multi_85b"),
    ("Teh volunteer organization helped thous4nds of families", 2, "multi_85c"),
    ("Teh voIunteer organizati0n heIped thous4nds of farnilies", 3, "multi_85d"),
    # ── base 86 ──
    ("The infrastrudure requirecl significant investrnent", 2, "multi_86a"),
    ("Teh infrastructure required signific4nt investment", 2, "multi_86b"),
    ("The infrastrudure required significant investrnent", 2, "multi_86c"),
    ("Teh infrastrudure requirecl signific4nt investrnent", 3, "multi_86d"),
    # ── base 87 ──
    ("Teh professor explalined the cornplex rnathematical concept", 2, "multi_87a"),
    ("The professor explained the cornplex rnathernatical concept", 2, "multi_87b"),
    ("Teh professor explained teh complex mathematical conc3pt", 2, "multi_87c"),
    ("Teh professor explalined the cornplex rnathernatical conc3pt", 3, "multi_87d"),
    # ── base 88 ──
    ("The electi0n cornrnission verifiecl the results", 2, "multi_88a"),
    ("Teh election commission verified teh results", 2, "multi_88b"),
    ("The electi0n commission verifiecl the resuIts", 2, "multi_88c"),
    ("Teh electi0n cornrnission verifiecl teh resuIts", 3, "multi_88d"),
    # ── base 89 ──
    ("The rnuseum's coIIection indudecl rare artifacts", 2, "multi_89a"),
    ("Teh museum's collection incIuded rare artif4cts", 2, "multi_89b"),
    ("The rnuseum's collection included rar3 artifacts", 2, "multi_89c"),
    ("Teh rnuseum's coIIection indudecl rar3 artif4cts", 3, "multi_89d"),
    # ── base 90 ──
    ("Teh governrnent spokesperson issuecl a clarification", 2, "multi_90a"),
    ("The governrnent spok3sperson issued a clarification", 2, "multi_90b"),
    ("Teh government spokesperson issued a darification", 2, "multi_90c"),
    ("Teh governrnent spok3sperson issuecl a darification", 3, "multi_90d"),
    # ── base 91 ──
    ("The particuIar spectade drew considerabie attention", 2, "multi_91a"),
    ("Teh particular spectacle drevv considerable att3ntion", 2, "multi_91b"),
    ("The particuIar spectacle drew considerabIe attention", 2, "multi_91c"),
    ("Teh particuIar spectade drevv considerabIe att3ntion", 3, "multi_91d"),
    # ── base 92 ──
    ("The diplornat addressecl the internationaI conference", 2, "multi_92a"),
    ("Teh diplomat addressed the international conf3rence", 2, "multi_92b"),
    ("The diplornat addressed teh international conference", 2, "multi_92c"),
    ("Teh diplornat addressecl teh internationaI conf3rence", 3, "multi_92d"),
    # ── base 93 ──
    ("Teh financiaI rnarket experiencecl unprecedented growth", 2, "multi_93a"),
    ("The financial market experienced unpreced3nted grovvth", 2, "multi_93b"),
    ("Teh financiaI market experienced unprecedented growth", 2, "multi_93c"),
    ("Teh financiaI rnarket experiencecl unpreced3nted grovvth", 3, "multi_93d"),
    # ── base 94 ──
    ("Teh governrnent fundecl the environmentaI research program", 2, "multi_94a"),
    ("The government funded the environrnental res3arch program", 2, "multi_94b"),
    ("Teh government fundecl the environmental research progr4m", 2, "multi_94c"),
    ("Teh governrnent fundecl the environrnentaI res3arch progr4m", 3, "multi_94d"),
    # ── base 95 ──
    ("The nurnerical data revealecl a significant trend", 2, "multi_95a"),
    ("Teh numerical clata reveaIed a significant tr3nd", 2, "multi_95b"),
    ("The nurnerical data revealed a signific4nt trend", 2, "multi_95c"),
    ("Teh nurnerical clata revealecl a signific4nt tr3nd", 3, "multi_95d"),
    # ── base 96 ──
    ("The corrrpany launchled a new cornrnercial product", 2, "multi_96a"),
    ("Teh company Iaunched a new commercial pr0duct", 2, "multi_96b"),
    ("The corrrpany launched a nevv commercial product", 2, "multi_96c"),
    ("Teh corrrpany launchled a nevv cornrnercial pr0duct", 3, "multi_96d"),
    # ── base 97 ──
    ("The dernonstrators rnarched through the tovvn peacefully", 2, "multi_97a"),
    ("Teh demonstrators marched thr0ugh the town peac3fully", 2, "multi_97b"),
    ("The dernonstrators marched through teh town peacefully", 2, "multi_97c"),
    ("Teh dernonstrators rnarched thr0ugh the tovvn peac3fully", 3, "multi_97d"),
    # ── base 98 ──
    ("Teh schoiarship prograrrr supportecl talented students", 2, "multi_98a"),
    ("The scholarship program supp0rted taIented students", 2, "multi_98b"),
    ("Teh scholarship program supported talented stud3nts", 2, "multi_98c"),
    ("Teh schoiarship prograrrr supp0rted taIented stud3nts", 3, "multi_98d"),
    # ── base 99 ──
    ("The reforrn proposal was debatecl in the Iegislature", 2, "multi_99a"),
    ("Teh reform proposai was debated in the legislature", 2, "multi_99b"),
    ("The reforrn proposal vvas debated in the legislature", 2, "multi_99c"),
    ("Teh reforrn proposai vvas debatecl in the Iegislature", 3, "multi_99d"),
    # ── base 100 ──
    ("The internationaI cornrnission reviewecl trade policies", 2, "multi_100a"),
    ("Teh international commission revievved trade poIicies", 2, "multi_100b"),
    ("The internationaI commission reviewed tracl3 policies", 2, "multi_100c"),
    ("Teh internationaI cornrnission revievved tracl3 poIicies", 3, "multi_100d"),
]


@pytest.mark.integration
@pytest.mark.ocr_positive
@pytest.mark.parametrize("text,min_spans,test_id", MULTI_ERROR_CASES)
def test_ocr_multi_error(text, min_spans, test_id, api):
    body = ocr_check(api, text)
    assert body["result"] == "issue_detected", (
        f"[{test_id}] Should detect multiple errors"
    )
    assert len(body.get("spans", [])) >= min_spans, (
        f"[{test_id}] Expected >= {min_spans} spans, got {len(body.get('spans', []))}"
    )


# ═══════════════════════════════════════════════════════════════════════
# 4. HARD / TRICKY TRUE POSITIVES  (400 tests)
# ═══════════════════════════════════════════════════════════════════════

HARD_CASES = [
    # ── Single error in long text (error diluted by clean context) ─────
    (
        "The national infrastructure plan included provisions for bridge repair, road maintenance, highway expansion, and the modernization of the cornrnunication network across three states",
        "cornrnunication", "communication", "hard_long_ctx_1",
    ),
    (
        "After careful consideration of all available evidence, the committee members voted unanimously to approve the proposed arnendment to the existing charter",
        "arnendment", "amendment", "hard_long_ctx_2",
    ),
    (
        "The university announced that the new research facility would be open to students and faculty starting next semester, with the experirnental labs available by spring",
        "experirnental", "experimental", "hard_long_ctx_3",
    ),
    (
        "Local residents gathered at the town hall meeting to discuss a variety of topics including zoning regulations, property taxes, and the proposed developrnent project on the east side of the river",
        "developrnent", "development", "hard_long_ctx_4",
    ),
    (
        "The annual report detailed strong revenue growth across all divisions including manufacturing, distribution, marketing, sales, and custorner service departments",
        "custorner", "customer", "hard_long_ctx_5",
    ),
    (
        "The hospital administration released a statement noting that patient satisfaction scores had improved significantly thanks to the dedication of the rnedical staff and support personnel",
        "rnedical", "medical", "hard_long_ctx_6",
    ),
    (
        "During the ceremony, the governor praised the efforts of emergency responders who worked tirelessly through the night to protect the cornrnunity from the approaching wildfire",
        "cornrnunity", "community", "hard_long_ctx_7",
    ),
    (
        "The museum's latest exhibition featured artwork from over twenty countries, spanning centuries of cultural history and artistic developrnent from the Renaissance to modern times",
        "developrnent", "development", "hard_long_ctx_8",
    ),
    (
        "Economists predicted that the central bank's decision to raise interest rates would have a significant irnpact on the housing market over the following quarters",
        "irnpact", "impact", "hard_long_ctx_9",
    ),
    (
        "The software company released a comprehensive update addressing security vulnerabilities, performance issues, and several user interface irnprovements requested by the community",
        "irnprovements", "improvements", "hard_long_ctx_10",
    ),
    (
        "The archaeological team spent three years excavating the ancient site before publishing their findings about early hurnan settlements in the region near the mountain range",
        "hurnan", "human", "hard_long_ctx_11",
    ),
    (
        "Representatives from twelve nations convened to discuss climate policy, renewable energy investments, and the long-term sustainability of the global environrnent for future generations",
        "environrnent", "environment", "hard_long_ctx_12",
    ),
    (
        "The transportation authority confirmed that the new subway extension would serve an estimated forty thousand daily commuters once the terrninal station was completed next year",
        "terrninal", "terminal", "hard_long_ctx_13",
    ),
    (
        "The literary festival brought together authors, publishers, editors, and readers from around the world to celebrate creative writing and explore new experirnental genres",
        "experirnental", "experimental", "hard_long_ctx_14",
    ),
    (
        "The city council approved a budget of fifty million dollars for parks, recreation centers, street lighting, public transit, and cornrnunity health programs for the upcoming fiscal year",
        "cornrnunity", "community", "hard_long_ctx_15",
    ),
    (
        "After months of deliberation the regulatory board decided that the pharmaceutical company must conduct additional clinical trials before the new rnedicine could receive final approval",
        "rnedicine", "medicine", "hard_long_ctx_16",
    ),
    (
        "The energy company invested heavily in solar panel technology, wind turbines, and battery storage solutions to meet the increasing dernand for renewable power sources",
        "dernand", "demand", "hard_long_ctx_17",
    ),
    (
        "Volunteers from the nonprofit organization distributed food and supplies to families affected by the flooding, demonstrating the irnportance of community solidarity in times of crisis",
        "irnportance", "importance", "hard_long_ctx_18",
    ),
    (
        "The new highway bypass reduced travel time between the two cities by nearly thirty minutes and significantly decreased traffic congestion in the residential areas near the old govemment buildings",
        "govemment", "government", "hard_long_ctx_19",
    ),
    (
        "The school district implemented a comprehensive teacher training program focusing on modern pedagogy, digital literacy, and inclusive classroom rnethods that support all learners",
        "rnethods", "methods", "hard_long_ctx_20",
    ),
    # ── Error in uncommon / technical words ────────────────────────────
    (
        "The spectrophotorneter measured the absorbance of the solution accurately",
        "spectrophotorneter", "spectrophotometer", "hard_tech_1",
    ),
    (
        "The electrocardiograrr revealed abnormal heart rhythms in the patient",
        "electrocardiograrr", "electrocardiogram", "hard_tech_2",
    ),
    (
        "The therrnodynamic analysis predicted the system's equilibrium state",
        "therrnodynamic", "thermodynamic", "hard_tech_3",
    ),
    (
        "The spectrornetry results confirmed the presence of trace elements",
        "spectrornetry", "spectrometry", "hard_tech_4",
    ),
    (
        "The irnrnunological response was studied using advanced biomarkers",
        "irnrnunological", "immunological", "hard_tech_5",
    ),
    (
        "The geornetric properties of the crystal were carefully documented",
        "geornetric", "geometric", "hard_tech_6",
    ),
    (
        "The pharrnaceutical compound showed promising results in trials",
        "pharrnaceutical", "pharmaceutical", "hard_tech_7",
    ),
    (
        "The electrornagnetic field measurements exceeded expected values",
        "electrornagnetic", "electromagnetic", "hard_tech_8",
    ),
    (
        "The biochernical pathway was disrupted by the experimental compound",
        "biochernical", "biochemical", "hard_tech_9",
    ),
    (
        "The therrnoplastic material withstood temperatures above three hundred degrees",
        "therrnoplastic", "thermoplastic", "hard_tech_10",
    ),
    (
        "The chronorneter was calibrated before the precision experiment began",
        "chronorneter", "chronometer", "hard_tech_11",
    ),
    (
        "The algorithrn was optimized for large-scale data processing tasks",
        "algorithrn", "algorithm", "hard_tech_12",
    ),
    (
        "The photovoltalc cells converted sunlight into electrical energy",
        "photovoltalc", "photovoltaic", "hard_tech_13",
    ),
    (
        "The rnicroprocessor executed billions of instructions per second",
        "rnicroprocessor", "microprocessor", "hard_tech_14",
    ),
    (
        "The infrastruclure supported high-bandwidth data transmission",
        "infrastruclure", "infrastructure", "hard_tech_15",
    ),
    (
        "The cardiovascuIar system was examined using ultrasound imaging",
        "cardiovascuIar", "cardiovascular", "hard_tech_16",
    ),
    (
        "The serniconductor chip was manufactured using advanced lithography",
        "serniconductor", "semiconductor", "hard_tech_17",
    ),
    (
        "The polyrner chain reaction was completed in under two hours",
        "polyrner", "polymer", "hard_tech_18",
    ),
    (
        "The neurochernistry of the brain was the focus of the new study",
        "neurochernistry", "neurochemistry", "hard_tech_19",
    ),
    (
        "The geornetry of the nano-structures was analyzed by electron microscopy",
        "geornetry", "geometry", "hard_tech_20",
    ),
    # ── Error at start of text ─────────────────────────────────────────
    (
        "Governrnent officials announced new regulations yesterday",
        "Governrnent", "Government", "hard_start_1",
    ),
    (
        "Cornrnunity leaders gathered to discuss the proposal",
        "Cornrnunity", "Community", "hard_start_2",
    ),
    (
        "Environrnental protection remains a top priority",
        "Environrnental", "Environmental", "hard_start_3",
    ),
    (
        "Developrnent of the new facility has begun on schedule",
        "Developrnent", "Development", "hard_start_4",
    ),
    (
        "Experirnental data confirmed the hypothesis was correct",
        "Experirnental", "Experimental", "hard_start_5",
    ),
    (
        "Cornrnercial activity increased sharply in the third quarter",
        "Cornrnercial", "Commercial", "hard_start_6",
    ),
    (
        "Fundarnental rights must be protected under all circumstances",
        "Fundarnental", "Fundamental", "hard_start_7",
    ),
    (
        "Recornrnendations from the panel were adopted immediately",
        "Recornrnendations", "Recommendations", "hard_start_8",
    ),
    (
        "Perrnanent changes to the tax code were implemented this year",
        "Perrnanent", "Permanent", "hard_start_9",
    ),
    (
        "Instrurnents were calibrated before the experiment started",
        "Instrurnents", "Instruments", "hard_start_10",
    ),
    (
        "Tovver construction was delayed due to material shortages",
        "Tovver", "Tower", "hard_start_11",
    ),
    (
        "Hovvever the committee decided to proceed with the plan",
        "Hovvever", "However", "hard_start_12",
    ),
    (
        "Wihtout proper funding the project cannot continue",
        "Wihtout", "Without", "hard_start_13",
    ),
    (
        "Becuase of the storm the event was postponed indefinitely",
        "Becuase", "Because", "hard_start_14",
    ),
    (
        "Alraedy the results have exceeded initial expectations",
        "Alraedy", "Already", "hard_start_15",
    ),
    (
        "Perhpas the most significant finding was in chapter three",
        "Perhpas", "Perhaps", "hard_start_16",
    ),
    (
        "Shoudl the proposal be approved it will take effect in July",
        "Shoudl", "Should", "hard_start_17",
    ),
    (
        "Thougth the evidence was circumstantial it proved convincing",
        "Thougth", "Thought", "hard_start_18",
    ),
    (
        "Teh president addressed the nation during the evening broadcast",
        "Teh", "The", "hard_start_19",
    ),
    (
        "Taht was the conclusion reached by the independent auditor",
        "Taht", "That", "hard_start_20",
    ),
    # ── Error at end of text ───────────────────────────────────────────
    (
        "The document was reviewed by the entire governrnent",
        "governrnent", "government", "hard_end_1",
    ),
    (
        "The mayor praised the resilience of the cornrnunity",
        "cornrnunity", "community", "hard_end_2",
    ),
    (
        "The study focused on the natural environrnent",
        "environrnent", "environment", "hard_end_3",
    ),
    (
        "The project made significant progress in developrnent",
        "developrnent", "development", "hard_end_4",
    ),
    (
        "The lab was dedicated to experirnental",
        "experirnental", "experimental", "hard_end_5",
    ),
    (
        "The plan included a cornrnercial",
        "cornrnercial", "commercial", "hard_end_6",
    ),
    (
        "The company released an official staternent",
        "staternent", "statement", "hard_end_7",
    ),
    (
        "The agency issued a new requirernent",
        "requirernent", "requirement", "hard_end_8",
    ),
    (
        "The evidence led to a startling achievernent",
        "achievernent", "achievement", "hard_end_9",
    ),
    (
        "The speaker received the highest cornplirnent",
        "cornplirnent", "compliment", "hard_end_10",
    ),
    (
        "The bridge was considered a national monurnent",
        "monurnent", "monument", "hard_end_11",
    ),
    (
        "He was recognized as a leading experirnent",
        "experirnent", "experiment", "hard_end_12",
    ),
    (
        "The data was analyzed using a new instrurnent",
        "instrurnent", "instrument", "hard_end_13",
    ),
    (
        "The election was decided by a narrow rnargin",
        "rnargin", "margin", "hard_end_14",
    ),
    (
        "The council debated the proposed arnendrnent",
        "arnendrnent", "amendment", "hard_end_15",
    ),
    (
        "The festival attracted visitors from every tovvn",
        "tovvn", "town", "hard_end_16",
    ),
    (
        "The athlete set a record that was widely knovvn",
        "knovvn", "known", "hard_end_17",
    ),
    (
        "She wore a beautiful silk govvn",
        "govvn", "gown", "hard_end_18",
    ),
    (
        "The child learned to count from one to dovvn",
        "dovvn", "down", "hard_end_19",
    ),
    (
        "The court hearing was scheduled for the afternoorn",
        "afternoorn", "afternoon", "hard_end_20",
    ),
    # ── Error adjacent to punctuation ──────────────────────────────────
    (
        'The report stated: "The governrnent must act now."',
        "governrnent", "government", "hard_punct_1",
    ),
    (
        "After the experirnent, researchers published their results.",
        "experirnent", "experiment", "hard_punct_2",
    ),
    (
        "The environrnent—already fragile—needed immediate protection.",
        "environrnent", "environment", "hard_punct_3",
    ),
    (
        "Was the developrnent approved by the board?",
        "developrnent", "development", "hard_punct_4",
    ),
    (
        "The cornrnittee (formed last year) released its findings.",
        "cornrnittee", "committee", "hard_punct_5",
    ),
    (
        'She described the event as "spectadular," drawing applause.',
        "spectadular", "spectacular", "hard_punct_6",
    ),
    (
        "The list included: apples, oranges, and brovvn sugar.",
        "brovvn", "brown", "hard_punct_7",
    ),
    (
        "Is the cornrnunication system working properly?",
        "cornrnunication", "communication", "hard_punct_8",
    ),
    (
        "The cornrnand—once given—cannot be revoked.",
        "cornrnand", "command", "hard_punct_9",
    ),
    (
        '"The instrurnent is precise," the technician confirmed.',
        "instrurnent", "instrument", "hard_punct_10",
    ),
    (
        "After the tourrnarment, players celebrated their victory.",
        "tourrnarment", "tournament", "hard_punct_11",
    ),
    (
        "The rnaterial (imported from overseas) was expensive.",
        "rnaterial", "material", "hard_punct_12",
    ),
    (
        'He said, "The perrnanent solution requires more funding."',
        "perrnanent", "permanent", "hard_punct_13",
    ),
    (
        "The hurnan resources department—understaffed and overworked—struggled daily.",
        "hurnan", "human", "hard_punct_14",
    ),
    (
        "Can we confirrn the delivery date?",
        "confirrn", "confirm", "hard_punct_15",
    ),
    (
        "The platforrn, designed for scalability, handled the load.",
        "platforrn", "platform", "hard_punct_16",
    ),
    (
        '"The reforrn is necessary," the senator argued.',
        "reforrn", "reform", "hard_punct_17",
    ),
    (
        "The uniforrn—worn by all employees—was recently updated.",
        "uniforrn", "uniform", "hard_punct_18",
    ),
    (
        "Have you reviewed the docurnent?",
        "docurnent", "document", "hard_punct_19",
    ),
    (
        "The alarnm (installed last month) triggered at midnight.",
        "alarnm", "alarm", "hard_punct_20",
    ),
    # ── Error in word next to a legitimate number ──────────────────────
    (
        "The cornrnittee reviewed 47 applications last week",
        "cornrnittee", "committee", "hard_num_1",
    ),
    (
        "Over 200 residents attended the governrnent hearing",
        "governrnent", "government", "hard_num_2",
    ),
    (
        "The experirnent involved 16 separate trials",
        "experirnent", "experiment", "hard_num_3",
    ),
    (
        "They collected 3,500 sarnples from the river basin",
        "sarnples", "samples", "hard_num_4",
    ),
    (
        "The developrnent will span 120 acres of land",
        "developrnent", "development", "hard_num_5",
    ),
    (
        "Approximately 85 rnillion people were affected by the policy",
        "rnillion", "million", "hard_num_6",
    ),
    (
        "The cornpany earned $4.2 rnillion in the first quarter",
        "rnillion", "million", "hard_num_7",
    ),
    (
        "Chapter 12 discusses the environrnent in detail",
        "environrnent", "environment", "hard_num_8",
    ),
    (
        "Section 5.3 describes the instrurnent calibration process",
        "instrurnent", "instrument", "hard_num_9",
    ),
    (
        "The tovver stands at 324 meters above sea level",
        "tovver", "tower", "hard_num_10",
    ),
    (
        "In 2024 the cornrnission published its annual review",
        "cornrnission", "commission", "hard_num_11",
    ),
    (
        "The 15 rnernbers of the committee voted unanimously",
        "rnernbers", "members", "hard_num_12",
    ),
    (
        "Page 43 contains the experirnental methodology",
        "experirnental", "experimental", "hard_num_13",
    ),
    (
        "The platforrn processed 10,000 transactions per second",
        "platforrn", "platform", "hard_num_14",
    ),
    (
        "The 8 departrments reported their quarterly results",
        "departrments", "departments", "hard_num_15",
    ),
    (
        "Unit 7 was assigned to the crirninal investigation",
        "crirninal", "criminal", "hard_num_16",
    ),
    (
        "The 2023 annual rnernorial ceremony was well attended",
        "rnernorial", "memorial", "hard_num_17",
    ),
    (
        "Room 301 housed the experirnental equipment",
        "experirnental", "experimental", "hard_num_18",
    ),
    (
        "Article 9 addressed the fundarnental rights of citizens",
        "fundarnental", "fundamental", "hard_num_19",
    ),
    (
        "The 500 participants cornpleted the survey on time",
        "cornpleted", "completed", "hard_num_20",
    ),
    # ── Very short text with error (3-5 words) ─────────────────────────
    (
        "Governrnent policy update today",
        "Governrnent", "Government", "hard_short_1",
    ),
    (
        "See the developrnent plan",
        "developrnent", "development", "hard_short_2",
    ),
    (
        "Contact the cornrnittee chair",
        "cornrnittee", "committee", "hard_short_3",
    ),
    (
        "Environrnent protection notice",
        "Environrnent", "Environment", "hard_short_4",
    ),
    (
        "Review the docurnent carefully",
        "docurnent", "document", "hard_short_5",
    ),
    (
        "Cornrnunity meeting tonight",
        "Cornrnunity", "Community", "hard_short_6",
    ),
    (
        "Experirnental results available",
        "Experirnental", "Experimental", "hard_short_7",
    ),
    (
        "Instrurnent calibration required",
        "Instrurnent", "Instrument", "hard_short_8",
    ),
    (
        "Perrnanent closure notice",
        "Perrnanent", "Permanent", "hard_short_9",
    ),
    (
        "Tovver inspection scheduled",
        "Tovver", "Tower", "hard_short_10",
    ),
    (
        "Recornrnendation report enclosed",
        "Recornrnendation", "Recommendation", "hard_short_11",
    ),
    (
        "Departrment budget review",
        "Departrment", "Department", "hard_short_12",
    ),
    (
        "Fundarnental rights declaration",
        "Fundarnental", "Fundamental", "hard_short_13",
    ),
    (
        "Cornrnercial lease agreement",
        "Cornrnercial", "Commercial", "hard_short_14",
    ),
    (
        "Nurnerical analysis report",
        "Nurnerical", "Numerical", "hard_short_15",
    ),
    (
        "Teh updated schedule",
        "Teh", "The", "hard_short_16",
    ),
    (
        "Wihtout further notice",
        "Wihtout", "Without", "hard_short_17",
    ),
    (
        "Becuase of delays",
        "Becuase", "Because", "hard_short_18",
    ),
    (
        "Shoudl be approved",
        "Shoudl", "Should", "hard_short_19",
    ),
    (
        "Alraedy in progress",
        "Alraedy", "Already", "hard_short_20",
    ),
    # ── Error that creates another valid word (wrong in context) ───────
    (
        "The police were called to the scene of the crirne",
        "crirne", "crime", "hard_realword_1",
    ),
    (
        "The nation celebrated its independence with a grand cererrony",
        "cererrony", "ceremony", "hard_realword_2",
    ),
    (
        "The soldiers were expected to perforrn their duties diligently",
        "perforrn", "perform", "hard_realword_3",
    ),
    (
        "She was asked to confirrn her attendance at the conference",
        "confirrn", "confirm", "hard_realword_4",
    ),
    (
        "The architects designed a uniforrn facade for the buildings",
        "uniforrn", "uniform", "hard_realword_5",
    ),
    (
        "The workers needed to reforrn the outdated procedures",
        "reforrn", "reform", "hard_realword_6",
    ),
    (
        "The company planned to transforrn its business model entirely",
        "transforrn", "transform", "hard_realword_7",
    ),
    (
        "The teacher asked students to perforrn the experiment carefully",
        "perforrn", "perform", "hard_realword_8",
    ),
    (
        "They used the platforrn to launch the new application",
        "platforrn", "platform", "hard_realword_9",
    ),
    (
        "The doctor needed to inforrn the patient about the results",
        "inforrn", "inform", "hard_realword_10",
    ),
    (
        "The committee could not condude the hearing on time",
        "condude", "conclude", "hard_realword_11",
    ),
    (
        "The report sought to indude all relevant data points",
        "indude", "include", "hard_realword_12",
    ),
    (
        "Officials voted to exdude the contested provision",
        "exdude", "exclude", "hard_realword_13",
    ),
    (
        "The agency planned to disdose the findings next week",
        "disdose", "disclose", "hard_realword_14",
    ),
    (
        "He managed to dedare his position clearly at the meeting",
        "dedare", "declare", "hard_realword_15",
    ),
    (
        "The brovvn envelope contained the classified documents",
        "brovvn", "brown", "hard_realword_16",
    ),
    (
        "The crovvn jewels were displayed under heavy security",
        "crovvn", "crown", "hard_realword_17",
    ),
    (
        "The city was widely knovvn for its historic architecture",
        "knovvn", "known", "hard_realword_18",
    ),
    (
        "The old tovvn square was renovated last summer",
        "tovvn", "town", "hard_realword_19",
    ),
    (
        "The child was grovvn enough to attend school independently",
        "grovvn", "grown", "hard_realword_20",
    ),
    # ── Multiple possible corrections ──────────────────────────────────
    (
        "The accornrnodation was comfortable and affordable",
        "accornrnodation", "accommodation", "hard_multi_corr_1",
    ),
    (
        "The adrninistration handled the crisis professionally",
        "adrninistration", "administration", "hard_multi_corr_2",
    ),
    (
        "The accornplishment was celebrated by the entire school",
        "accornplishment", "accomplishment", "hard_multi_corr_3",
    ),
    (
        "The irnplernentation phase took longer than expected",
        "irnplernentation", "implementation", "hard_multi_corr_4",
    ),
    (
        "The docurnentation was incomplete and needed updates",
        "docurnentation", "documentation", "hard_multi_corr_5",
    ),
    (
        "The proclarnation was read aloud at the ceremony",
        "proclarnation", "proclamation", "hard_multi_corr_6",
    ),
    (
        "The exarnination results will be posted tomorrow",
        "exarnination", "examination", "hard_multi_corr_7",
    ),
    (
        "The accurnulation of debt became a serious concern",
        "accurnulation", "accumulation", "hard_multi_corr_8",
    ),
    (
        "The transforrrnation of the industry took decades",
        "transforrrnation", "transformation", "hard_multi_corr_9",
    ),
    (
        "The approxirnation was close enough for the calculation",
        "approxirnation", "approximation", "hard_multi_corr_10",
    ),
    (
        "The deterrnination of the cause required extensive testing",
        "deterrnination", "determination", "hard_multi_corr_11",
    ),
    (
        "The cornrnunication breakdown led to the misunderstanding",
        "cornrnunication", "communication", "hard_multi_corr_12",
    ),
    (
        "The recornrnendation was to increase the annual budget",
        "recornrnendation", "recommendation", "hard_multi_corr_13",
    ),
    (
        "The adrninistrative burden fell on the local office",
        "adrninistrative", "administrative", "hard_multi_corr_14",
    ),
    (
        "The phenornenon was observed across multiple studies",
        "phenornenon", "phenomenon", "hard_multi_corr_15",
    ),
    (
        "The cornpetition attracted participants from every region",
        "cornpetition", "competition", "hard_multi_corr_16",
    ),
    (
        "The rnisunderstanding arose from a lack of communication",
        "rnisunderstanding", "misunderstanding", "hard_multi_corr_17",
    ),
    (
        "The accornpanying materials were distributed at the door",
        "accornpanying", "accompanying", "hard_multi_corr_18",
    ),
    (
        "The rnanufacturer recalled thousands of defective units",
        "rnanufacturer", "manufacturer", "hard_multi_corr_19",
    ),
    (
        "The environrnental assessment was completed on schedule",
        "environrnental", "environmental", "hard_multi_corr_20",
    ),
    # ── Error in capitalized word ──────────────────────────────────────
    (
        "The United Nations Environrnent Programme released a new report",
        "Environrnent", "Environment", "hard_cap_1",
    ),
    (
        "The European Cornrnission proposed updated regulations",
        "Cornrnission", "Commission", "hard_cap_2",
    ),
    (
        "The Federal Governrnent allocated emergency funding",
        "Governrnent", "Government", "hard_cap_3",
    ),
    (
        "The National Developrnent Council convened an emergency session",
        "Developrnent", "Development", "hard_cap_4",
    ),
    (
        "The Departrnent of Education announced new standards",
        "Departrnent", "Department", "hard_cap_5",
    ),
    (
        "The International Cornrnittee met in Geneva last month",
        "Cornrnittee", "Committee", "hard_cap_6",
    ),
    (
        "The National Monurnent was restored to its original condition",
        "Monurnent", "Monument", "hard_cap_7",
    ),
    (
        "The World Environrnent Day celebration was held in June",
        "Environrnent", "Environment", "hard_cap_8",
    ),
    (
        "The Cornrnunity Development Foundation supported local projects",
        "Cornrnunity", "Community", "hard_cap_9",
    ),
    (
        "The Perrnanent Court of Arbitration issued its ruling",
        "Perrnanent", "Permanent", "hard_cap_10",
    ),
    (
        "GOVERNRNENT OFFICIALS RELEASED THE CLASSIFIED REPORT",
        "GOVERNRNENT", "GOVERNMENT", "hard_cap_11",
    ),
    (
        "CORNRNUNITY LEADERS MET TO DISCUSS THE PROPOSAL",
        "CORNRNUNITY", "COMMUNITY", "hard_cap_12",
    ),
    (
        "THE DEVELOPRNENT PROJECT WAS APPROVED UNANIMOUSLY",
        "DEVELOPRNENT", "DEVELOPMENT", "hard_cap_13",
    ),
    (
        "THE EXPERIRNENTAL RESULTS EXCEEDED ALL EXPECTATIONS",
        "EXPERIRNENTAL", "EXPERIMENTAL", "hard_cap_14",
    ),
    (
        "THE CORNRNISSION VOTED ON THE NEW GUIDELINES TODAY",
        "CORNRNISSION", "COMMISSION", "hard_cap_15",
    ),
    (
        "The INSTRURNENT was designed for precision measurement",
        "INSTRURNENT", "INSTRUMENT", "hard_cap_16",
    ),
    (
        "President Johnson's Governrnent enacted the new legislation",
        "Governrnent", "Government", "hard_cap_17",
    ),
    (
        "The Fundarnental Rights Charter was ratified by all members",
        "Fundarnental", "Fundamental", "hard_cap_18",
    ),
    (
        "The Annual Tourrnarment drew competitors from twenty nations",
        "Tourrnarment", "Tournament", "hard_cap_19",
    ),
    (
        "The Cornrnercial District Revitalization Plan was launched",
        "Cornrnercial", "Commercial", "hard_cap_20",
    ),
    # ── Error in quoted text ───────────────────────────────────────────
    (
        'The report stated: "The governrnent must take action immediately."',
        "governrnent", "government", "hard_quote_1",
    ),
    (
        'She wrote in her letter: "The environrnent is our shared responsibility."',
        "environrnent", "environment", "hard_quote_2",
    ),
    (
        'The headline read: "Cornrnunity rallies behind local heroes."',
        "Cornrnunity", "Community", "hard_quote_3",
    ),
    (
        'His testimony included: "The experirnent was conducted safely."',
        "experirnent", "experiment", "hard_quote_4",
    ),
    (
        'The memo warned: "Developrnent must proceed with caution."',
        "Developrnent", "Development", "hard_quote_5",
    ),
    (
        'The sign read: "Perrnanent closure effective immediately."',
        "Perrnanent", "Permanent", "hard_quote_6",
    ),
    (
        'The manual stated: "The instrurnent requires daily calibration."',
        "instrurnent", "instrument", "hard_quote_7",
    ),
    (
        'The article noted: "The cornrnercial sector grew substantially."',
        "cornrnercial", "commercial", "hard_quote_8",
    ),
    (
        'The judge declared: "The arnendment is unconstitutional."',
        "arnendment", "amendment", "hard_quote_9",
    ),
    (
        'The spokesperson said: "The departrment is fully operational."',
        "departrment", "department", "hard_quote_10",
    ),
    (
        'The invitation stated: "The tourrnarment begins at noon."',
        "tourrnarment", "tournament", "hard_quote_11",
    ),
    (
        'The brochure promised: "A spectadular view from every room."',
        "spectadular", "spectacular", "hard_quote_12",
    ),
    (
        'Officials declared: "The platforrn is secure and stable."',
        "platforrn", "platform", "hard_quote_13",
    ),
    (
        'The teacher explained: "The experirnental method requires patience."',
        "experirnental", "experimental", "hard_quote_14",
    ),
    (
        'The contract specified: "The perrnanent staff will be retained."',
        "perrnanent", "permanent", "hard_quote_15",
    ),
    (
        'The advertisement claimed: "This is a fundarnental breakthrough."',
        "fundarnental", "fundamental", "hard_quote_16",
    ),
    (
        'The witness testified: "The docurnent was signed under duress."',
        "docurnent", "document", "hard_quote_17",
    ),
    (
        'The caption read: "A monurnent to national resilience."',
        "monurnent", "monument", "hard_quote_18",
    ),
    (
        'The plaque stated: "Dedicated to the rnernorial of fallen soldiers."',
        "rnernorial", "memorial", "hard_quote_19",
    ),
    (
        'The reviewer wrote: "The perforrnnance was absolutely outstanding."',
        "perforrnnance", "performance", "hard_quote_20",
    ),
    # ── Error in word with legitimate nearby numbers ───────────────────
    (
        "The 2025 budget docurnent was approved on January 15",
        "docurnent", "document", "hard_numctx_1",
    ),
    (
        "Floor 3 of the building housed the experirnental labs since 2019",
        "experirnental", "experimental", "hard_numctx_2",
    ),
    (
        "Between 1990 and 2020 the cornrnunity grew by 300 percent",
        "cornrnunity", "community", "hard_numctx_3",
    ),
    (
        "The 45-page docurnent summarized the 2024 fiscal year",
        "docurnent", "document", "hard_numctx_4",
    ),
    (
        "In paragraph 7.2 the arnendment specifies a 90-day period",
        "arnendment", "amendment", "hard_numctx_5",
    ),
    (
        "The $12.5 rnillion grant funded 8 research laboratories",
        "rnillion", "million", "hard_numctx_6",
    ),
    (
        "Table 4 on page 29 shows the experirnental data from 2023",
        "experirnental", "experimental", "hard_numctx_7",
    ),
    (
        "The 150-rnernber delegation arrived on March 3rd",
        "150-rnernber", "150-member", "hard_numctx_8",
    ),
    (
        "By 2030 the govemment plans to reduce emissions by 40 percent",
        "govemment", "government", "hard_numctx_9",
    ),
    (
        "The 1,200-seat auditorium hosted the tourrnarment finals in 2022",
        "tourrnarment", "tournament", "hard_numctx_10",
    ),
    # ── Mixed bag: more tricky true positives ──────────────────────────
    (
        "The judge's staterment was carefully worded to avoid ambiguity",
        "staterment", "statement", "hard_misc_1",
    ),
    (
        "According to the acadernic journal the findings were inconclusive",
        "acadernic", "academic", "hard_misc_2",
    ),
    (
        "The parIiament voted on the controversial legislation yesterday",
        "parIiament", "parliament", "hard_misc_3",
    ),
    (
        "The new ernployee completed the orientation program successfully",
        "ernployee", "employee", "hard_misc_4",
    ),
    (
        "Climate scientists studied the phenornenon for over a decade",
        "phenornenon", "phenomenon", "hard_misc_5",
    ),
    (
        "The rnanuscript was discovered in the basement of the old library",
        "rnanuscript", "manuscript", "hard_misc_6",
    ),
    (
        "The cornputer system crashed during the critical update process",
        "cornputer", "computer", "hard_misc_7",
    ),
    (
        "The suprerme court's decision was announced this morning",
        "suprerme", "supreme", "hard_misc_8",
    ),
    (
        "The accurnulated evidence overwhelmingly supported the theory",
        "accurnulated", "accumulated", "hard_misc_9",
    ),
    (
        "The assernbly line produced thousands of units every day",
        "assernbly", "assembly", "hard_misc_10",
    ),
    (
        "The rnajority of respondents supported the proposed change",
        "rnajority", "majority", "hard_misc_11",
    ),
    (
        "The telescope captured rermarkable images of the distant galaxy",
        "rermarkable", "remarkable", "hard_misc_12",
    ),
    (
        "The recomrnendation was to invest in renewable energy sources",
        "recomrnendation", "recommendation", "hard_misc_13",
    ),
    (
        "The rnilestone was reached ahead of the original schedule",
        "rnilestone", "milestone", "hard_misc_14",
    ),
    (
        "The perforrnance review highlighted areas for improvement",
        "perforrnance", "performance", "hard_misc_15",
    ),
    (
        "The new managernent team implemented sweeping reforms",
        "managernent", "management", "hard_misc_16",
    ),
    (
        "The advertiserment campaign reached millions of viewers",
        "advertiserment", "advertisement", "hard_misc_17",
    ),
    (
        "The arrangerment of the conference was handled professionally",
        "arrangerment", "arrangement", "hard_misc_18",
    ),
    (
        "The replacernent parts arrived within three business days",
        "replacernent", "replacement", "hard_misc_19",
    ),
    (
        "The enforcerrrent of the regulations began in September",
        "enforcerrrent", "enforcement", "hard_misc_20",
    ),
    (
        "The investrnent portfolio was diversified across sectors",
        "investrnent", "investment", "hard_misc_21",
    ),
    (
        "The settlerment agreement was reached after long negotiations",
        "settlerment", "settlement", "hard_misc_22",
    ),
    (
        "The entertainrnent industry adapted to streaming technology",
        "entertainrnent", "entertainment", "hard_misc_23",
    ),
    (
        "The equiprnent was inspected before the operation commenced",
        "equiprnent", "equipment", "hard_misc_24",
    ),
    (
        "The assessrnent tool was validated by independent experts",
        "assessrnent", "assessment", "hard_misc_25",
    ),
    (
        "The involvernent of local businesses boosted the economy",
        "involvernent", "involvement", "hard_misc_26",
    ),
    (
        "The advancernent of technology changed everyday life",
        "advancernent", "advancement", "hard_misc_27",
    ),
    (
        "The announcerrrent was made during the press conference",
        "announcerrrent", "announcement", "hard_misc_28",
    ),
    (
        "The achievernent was recognized by the international body",
        "achievernent", "achievement", "hard_misc_29",
    ),
    (
        "The improvernent in test scores delighted the teachers",
        "improvernent", "improvement", "hard_misc_30",
    ),
    (
        "The exciterment surrounding the discovery was palpable",
        "exciterment", "excitement", "hard_misc_31",
    ),
    (
        "The retirernent plan was available to all full-time staff",
        "retirernent", "retirement", "hard_misc_32",
    ),
    (
        "The engagernent with the local community was highly valued",
        "engagernent", "engagement", "hard_misc_33",
    ),
    (
        "The enlargernent of the facility doubled its capacity",
        "enlargernent", "enlargement", "hard_misc_34",
    ),
    (
        "The abandonrnent of the site raised environmental concerns",
        "abandonrnent", "abandonment", "hard_misc_35",
    ),
    (
        "The aligmnent of the satellite was completed successfully",
        "aligmnent", "alignment", "hard_misc_36",
    ),
    (
        "The detachrment was deployed to the northern border",
        "detachrment", "detachment", "hard_misc_37",
    ),
    (
        "The attachrnent included the full financial breakdown",
        "attachrnent", "attachment", "hard_misc_38",
    ),
    (
        "The procurernent office handled all vendor contracts",
        "procurernent", "procurement", "hard_misc_39",
    ),
    (
        "The deployrment was completed without major incidents",
        "deployrment", "deployment", "hard_misc_40",
    ),
    # ── Errors in possessives and contractions ─────────────────────────
    (
        "The cornpany's reputation was built on years of trust",
        "cornpany's", "company's", "hard_poss_1",
    ),
    (
        "The governrnent's response was swift and decisive",
        "governrnent's", "government's", "hard_poss_2",
    ),
    (
        "The cornrnunity's voice was heard during the public hearing",
        "cornrnunity's", "community's", "hard_poss_3",
    ),
    (
        "The departrment's budget was reduced by fifteen percent",
        "departrment's", "department's", "hard_poss_4",
    ),
    (
        "The cornrnittee's decision was announced at the press event",
        "cornrnittee's", "committee's", "hard_poss_5",
    ),
    (
        "The environrnent's fragility was highlighted in the study",
        "environrnent's", "environment's", "hard_poss_6",
    ),
    (
        "The cornpany's profits exceeded analyst expectations",
        "cornpany's", "company's", "hard_poss_7",
    ),
    (
        "The patient's treatrnent plan was updated by the specialist",
        "treatrnent", "treatment", "hard_poss_8",
    ),
    (
        "The nation's cornrnitment to peace was reaffirmed at the summit",
        "cornrnitment", "commitment", "hard_poss_9",
    ),
    (
        "The organization's rnanagement structure was overhauled completely",
        "rnanagement", "management", "hard_poss_10",
    ),
    # ── Errors in hyphenated words ─────────────────────────────────────
    (
        "The well-docurnented case was presented to the jury",
        "well-docurnented", "well-documented", "hard_hyph_1",
    ),
    (
        "The self-governrnent initiative was approved by the assembly",
        "self-governrnent", "self-government", "hard_hyph_2",
    ),
    (
        "The long-terrn investment strategy was revised this quarter",
        "long-terrn", "long-term", "hard_hyph_3",
    ),
    (
        "The state-of-the-art instrurnent was installed in the lab",
        "instrurnent", "instrument", "hard_hyph_4",
    ),
    (
        "A high-perforrnance engine was developed for the new model",
        "high-perforrnance", "high-performance", "hard_hyph_5",
    ),
    (
        "The multi-platforrn solution supported all major operating systems",
        "multi-platforrn", "multi-platform", "hard_hyph_6",
    ),
    (
        "The cross-exarnination lasted for over three hours",
        "cross-exarnination", "cross-examination", "hard_hyph_7",
    ),
    (
        "The non-cornrnercial license restricted certain uses",
        "non-cornrnercial", "non-commercial", "hard_hyph_8",
    ),
    (
        "The pre-experirnental phase involved extensive planning",
        "pre-experirnental", "pre-experimental", "hard_hyph_9",
    ),
    (
        "The inter-governrnental agreement was signed by twelve nations",
        "inter-governrnental", "inter-governmental", "hard_hyph_10",
    ),
    # ── Errors in plural and verb forms ────────────────────────────────
    (
        "The experirnents yielded promising results across all groups",
        "experirnents", "experiments", "hard_plural_1",
    ),
    (
        "Several governrnents signed the trade agreement last week",
        "governrnents", "governments", "hard_plural_2",
    ),
    (
        "The instrurnents were calibrated before each measurement",
        "instrurnents", "instruments", "hard_plural_3",
    ),
    (
        "All departrments submitted their quarterly reports on time",
        "departrments", "departments", "hard_plural_4",
    ),
    (
        "The cornrnittees met separately before the joint session",
        "cornrnittees", "committees", "hard_plural_5",
    ),
    (
        "New developrnents in the case surprised the legal team",
        "developrnents", "developments", "hard_plural_6",
    ),
    (
        "The environrnents studied ranged from arctic to tropical",
        "environrnents", "environments", "hard_plural_7",
    ),
    (
        "The docurnents were stored in a secure digital archive",
        "docurnents", "documents", "hard_plural_8",
    ),
    (
        "Multiple assessrnents confirmed the initial diagnosis",
        "assessrnents", "assessments", "hard_plural_9",
    ),
    (
        "The requirernents for certification were recently updated",
        "requirernents", "requirements", "hard_plural_10",
    ),
    (
        "The investrnents generated substantial returns for shareholders",
        "investrnents", "investments", "hard_plural_11",
    ),
    (
        "The experirnental procedures were documented in the appendix",
        "experirnental", "experimental", "hard_plural_12",
    ),
    (
        "The achievernents of the team were recognized at the ceremony",
        "achievernents", "achievements", "hard_plural_13",
    ),
    (
        "Multiple cornrnunities were affected by the flooding",
        "cornrnunities", "communities", "hard_plural_14",
    ),
    (
        "The irnprovements to the system reduced downtime significantly",
        "irnprovements", "improvements", "hard_plural_15",
    ),
    (
        "The rnanagers discussed the proposed organizational changes",
        "rnanagers", "managers", "hard_plural_16",
    ),
    (
        "The recornrnendations were implemented across all branches",
        "recornrnendations", "recommendations", "hard_plural_17",
    ),
    (
        "The staternents made by both parties contradicted each other",
        "staternents", "statements", "hard_plural_18",
    ),
    (
        "The cornrnands were executed in the correct sequence",
        "cornrnands", "commands", "hard_plural_19",
    ),
    (
        "The fundarnentals of the curriculum were revised last year",
        "fundarnentals", "fundamentals", "hard_plural_20",
    ),
    # ── Errors in past tense and -ing forms ────────────────────────────
    (
        "The team recornrnended a complete overhaul of the system",
        "recornrnended", "recommended", "hard_tense_1",
    ),
    (
        "The agency deterrnined that the violations were systematic",
        "deterrnined", "determined", "hard_tense_2",
    ),
    (
        "The project was cornpleted ahead of schedule and under budget",
        "cornpleted", "completed", "hard_tense_3",
    ),
    (
        "The cornrnittee exarnined the evidence for three consecutive days",
        "exarnined", "examined", "hard_tense_4",
    ),
    (
        "The factory was transforrned into a modern production facility",
        "transforrned", "transformed", "hard_tense_5",
    ),
    (
        "The investigation confirrned the initial suspicions",
        "confirrned", "confirmed", "hard_tense_6",
    ),
    (
        "The researchers perforrned over two hundred separate trials",
        "perforrned", "performed", "hard_tense_7",
    ),
    (
        "The data was inforrned by observations spanning five years",
        "inforrned", "informed", "hard_tense_8",
    ),
    (
        "The building was reforrned to meet new safety standards",
        "reforrned", "reformed", "hard_tense_9",
    ),
    (
        "The report was cornpiled from sources across twelve countries",
        "cornpiled", "compiled", "hard_tense_10",
    ),
    (
        "The organization was cornrnitting resources to the new initiative",
        "cornrnitting", "committing", "hard_tense_11",
    ),
    (
        "The engineers were perforrning routine maintenance checks",
        "perforrning", "performing", "hard_tense_12",
    ),
    (
        "The agency was rnonitoring the situation around the clock",
        "rnonitoring", "monitoring", "hard_tense_13",
    ),
    (
        "The team was exarnining the samples under strict protocols",
        "exarnining", "examining", "hard_tense_14",
    ),
    (
        "The committee was deterrnining the scope of the audit",
        "deterrnining", "determining", "hard_tense_15",
    ),
    (
        "The company was developrng new products for the Asian market",
        "developrng", "developing", "hard_tense_16",
    ),
    (
        "The scientists were accurnulating data over several months",
        "accurnulating", "accumulating", "hard_tense_17",
    ),
    (
        "The authorities were confirrning the identities of the passengers",
        "confirrning", "confirming", "hard_tense_18",
    ),
    (
        "The workers cornplained about unsafe working conditions",
        "cornplained", "complained", "hard_tense_19",
    ),
    (
        "The manager recornrnended that all staff attend the training",
        "recornrnended", "recommended", "hard_tense_20",
    ),
    # ── Additional number-adjacent context cases ───────────────────────
    (
        "Exactly 1,500 docurnents were processed before the deadline",
        "docurnents", "documents", "hard_numctx_11",
    ),
    (
        "The $8.7 rnillion contract was awarded to the lowest bidder",
        "rnillion", "million", "hard_numctx_12",
    ),
    (
        "On March 15 the cornrnittee released its 200-page report",
        "cornrnittee", "committee", "hard_numctx_13",
    ),
    (
        "The 72-hour experirnent produced statistically significant results",
        "experirnent", "experiment", "hard_numctx_14",
    ),
    (
        "Since 1998 the environrnent has deteriorated measurably",
        "environrnent", "environment", "hard_numctx_15",
    ),
    (
        "The survey of 4,000 ernployees revealed widespread dissatisfaction",
        "ernployees", "employees", "hard_numctx_16",
    ),
    (
        "Amendment 14 of the docurnent was the most controversial",
        "docurnent", "document", "hard_numctx_17",
    ),
    (
        "The platforrn handled over 25,000 concurrent users daily",
        "platforrn", "platform", "hard_numctx_18",
    ),
    (
        "Building 9 housed the experirnental research division",
        "experirnental", "experimental", "hard_numctx_19",
    ),
    (
        "The 60-day assessrnent period ended without incident",
        "assessrnent", "assessment", "hard_numctx_20",
    ),
    # ── Additional mixed difficult cases ───────────────────────────────
    (
        "The board's recornrnendation contradicted the staff analysis",
        "recornrnendation", "recommendation", "hard_misc_41",
    ),
    (
        "The systern was designed to handle peak loads efficiently",
        "systern", "system", "hard_misc_42",
    ),
    (
        "The prograrn was launched to support first-generation students",
        "prograrn", "program", "hard_misc_43",
    ),
    (
        "The problern was identified during the routine audit process",
        "problern", "problem", "hard_misc_44",
    ),
    (
        "The bottorn line showed a net loss for the third quarter",
        "bottorn", "bottom", "hard_misc_45",
    ),
    (
        "The randorn selection process ensured statistical validity",
        "randorn", "random", "hard_misc_46",
    ),
    (
        "The custorn software was developed to meet specific needs",
        "custorn", "custom", "hard_misc_47",
    ),
    (
        "The kingdorn prospered under the new ruler's leadership",
        "kingdorn", "kingdom", "hard_misc_48",
    ),
    (
        "The phantorn signal appeared intermittently on the radar",
        "phantorn", "phantom", "hard_misc_49",
    ),
    (
        "The wisclom of the decision was debated for years afterward",
        "wisclom", "wisdom", "hard_misc_50",
    ),
    # ── Errors in adverbs and adjectives ───────────────────────────────
    (
        "The cornpletely redesigned interface impressed the reviewers",
        "cornpletely", "completely", "hard_adv_1",
    ),
    (
        "The irnrnediately available resources were allocated to the team",
        "irnrnediately", "immediately", "hard_adv_2",
    ),
    (
        "The approxirnately three hundred guests arrived on time",
        "approxirnately", "approximately", "hard_adv_3",
    ),
    (
        "The perrnanently installed fixtures met building codes",
        "perrnanently", "permanently", "hard_adv_4",
    ),
    (
        "The experirnentally verified results were published promptly",
        "experirnentally", "experimentally", "hard_adv_5",
    ),
    (
        "The fundarnentally flawed approach was abandoned after review",
        "fundarnentally", "fundamentally", "hard_adv_6",
    ),
    (
        "The environrnentally conscious company reduced waste by half",
        "environrnentally", "environmentally", "hard_adv_7",
    ),
    (
        "The norrnally quiet neighborhood was disrupted by construction",
        "norrnally", "normally", "hard_adv_8",
    ),
    (
        "The forrrnally submitted proposal met all stated requirements",
        "forrrnally", "formally", "hard_adv_9",
    ),
    (
        "The rninimally invasive procedure reduced recovery time",
        "rninimally", "minimally", "hard_adv_10",
    ),
    # ── Errors in compound sentences ───────────────────────────────────
    (
        "The govemment released a statement, and the cornrnunity responded positively",
        "govemment", "government", "hard_compound_1",
    ),
    (
        "The experirnent concluded successfully, but the results need further analysis",
        "experirnent", "experiment", "hard_compound_2",
    ),
    (
        "Workers dernanded higher wages, so the cornpany began negotiations",
        "dernanded", "demanded", "hard_compound_3",
    ),
    (
        "The developrnent was on schedule, yet costs continued to rise",
        "developrnent", "development", "hard_compound_4",
    ),
    (
        "The instrurnent malfunctioned, and the experiment was delayed",
        "instrurnent", "instrument", "hard_compound_5",
    ),
    (
        "The tourrnarment was postponed, but organizers rescheduled quickly",
        "tourrnarment", "tournament", "hard_compound_6",
    ),
    (
        "The perrnanent staff were retained, while temporary workers were released",
        "perrnanent", "permanent", "hard_compound_7",
    ),
    (
        "The cornrnission investigated the matter, and published its findings",
        "cornrnission", "commission", "hard_compound_8",
    ),
    (
        "The platforrn was upgraded, so performance improved dramatically",
        "platforrn", "platform", "hard_compound_9",
    ),
    (
        "The rnaterial arrived late, but the project still finished on time",
        "rnaterial", "material", "hard_compound_10",
    ),
    # ── Errors in passive voice constructions ──────────────────────────
    (
        "The docurnent was approved by the senior management team",
        "docurnent", "document", "hard_passive_1",
    ),
    (
        "The experirnent was conducted by a team of graduate students",
        "experirnent", "experiment", "hard_passive_2",
    ),
    (
        "The cornrnand was issued by the regional headquarters",
        "cornrnand", "command", "hard_passive_3",
    ),
    (
        "The equiprnent was inspected by certified technicians",
        "equiprnent", "equipment", "hard_passive_4",
    ),
    (
        "The recornrnendation was endorsed by all board members",
        "recornrnendation", "recommendation", "hard_passive_5",
    ),
    (
        "The reforrn was championed by a coalition of civic groups",
        "reforrn", "reform", "hard_passive_6",
    ),
    (
        "The arnendment was ratified by the state legislature",
        "arnendment", "amendment", "hard_passive_7",
    ),
    (
        "The monurnent was dedicated by the governor herself",
        "monurnent", "monument", "hard_passive_8",
    ),
    (
        "The crirninal was sentenced by the federal court",
        "crirninal", "criminal", "hard_passive_9",
    ),
    (
        "The transforrn was applied by the automated pipeline",
        "transforrn", "transform", "hard_passive_10",
    ),
    # ── Errors in questions ────────────────────────────────────────────
    (
        "What is the current status of the developrnent project?",
        "developrnent", "development", "hard_question_1",
    ),
    (
        "Has the cornrnittee reached a final decision yet?",
        "cornrnittee", "committee", "hard_question_2",
    ),
    (
        "When will the experirnental phase be completed?",
        "experirnental", "experimental", "hard_question_3",
    ),
    (
        "How many docurnents were reviewed during the audit?",
        "docurnents", "documents", "hard_question_4",
    ),
    (
        "Why was the perrnanent closure not communicated sooner?",
        "perrnanent", "permanent", "hard_question_5",
    ),
    (
        "Did the cornrnission approve the proposed regulations?",
        "cornrnission", "commission", "hard_question_6",
    ),
    (
        "Where is the instrurnent calibration log stored?",
        "instrurnent", "instrument", "hard_question_7",
    ),
    (
        "Who authorized the departrment budget increase?",
        "departrment", "department", "hard_question_8",
    ),
    (
        "Can the platforrn handle the expected traffic volume?",
        "platforrn", "platform", "hard_question_9",
    ),
    (
        "Should the environrnental review be conducted first?",
        "environrnental", "environmental", "hard_question_10",
    ),
    # ── Errors in list-like / enumerated text ──────────────────────────
    (
        "The agenda included: budget review, staffing, cornrnunications, and logistics",
        "cornrnunications", "communications", "hard_list_1",
    ),
    (
        "Key topics: environrnent, education, healthcare, and housing",
        "environrnent", "environment", "hard_list_2",
    ),
    (
        "Required docurnents: passport, visa, insurance, and itinerary",
        "docurnents", "documents", "hard_list_3",
    ),
    (
        "The team comprised engineers, rnathematicians, physicists, and analysts",
        "rnathematicians", "mathematicians", "hard_list_4",
    ),
    (
        "Priority areas: infrastruclure, transportation, energy, and water",
        "infrastruclure", "infrastructure", "hard_list_5",
    ),
    (
        "The kit includes: therrometer, bandages, antiseptic, and gloves",
        "therrometer", "thermometer", "hard_list_6",
    ),
    (
        "Departments affected: finance, hurnan resources, IT, and legal",
        "hurnan", "human", "hard_list_7",
    ),
    (
        "Training modules: safety, cornpliance, ethics, and leadership",
        "cornpliance", "compliance", "hard_list_8",
    ),
    (
        "Sections: introduction, rnethodology, results, and discussion",
        "rnethodology", "methodology", "hard_list_9",
    ),
    (
        "Materials needed: therrnoplastic, adhesive, sealant, and primer",
        "therrnoplastic", "thermoplastic", "hard_list_10",
    ),
    # ── Errors in formal / legal register ──────────────────────────────
    (
        "Pursuant to Section 4, the governrnent shall provide adequate notice",
        "governrnent", "government", "hard_legal_1",
    ),
    (
        "The undersigned hereby confirrns receipt of the enclosed materials",
        "confirrns", "confirms", "hard_legal_2",
    ),
    (
        "Notwithstanding any provision to the contrary, the cornrnittee retains authority",
        "cornrnittee", "committee", "hard_legal_3",
    ),
    (
        "The respondent shall cornply with all terms of the injunction",
        "cornply", "comply", "hard_legal_4",
    ),
    (
        "In accordance with the arnendment, the deadline is extended by thirty days",
        "arnendment", "amendment", "hard_legal_5",
    ),
    (
        "The plaintiff alleges that the defenclant violated the agreement",
        "defenclant", "defendant", "hard_legal_6",
    ),
    (
        "Said docurnent shall be filed with the clerk within ten business days",
        "docurnent", "document", "hard_legal_7",
    ),
    (
        "The tribunal deterrnined that the claim was without merit",
        "deterrnined", "determined", "hard_legal_8",
    ),
    (
        "The perrnanent injunction shall remain in effect until further order",
        "perrnanent", "permanent", "hard_legal_9",
    ),
    (
        "The cornrnission shall have jurisdiction over all related matters",
        "cornrnission", "commission", "hard_legal_10",
    ),
]


@pytest.mark.integration
@pytest.mark.ocr_positive
@pytest.mark.parametrize(
    "text,error_word,expected_correction,test_id", HARD_CASES
)
def test_ocr_hard_case(text, error_word, expected_correction, test_id, api):
    body = ocr_check(api, text)
    assert body["result"] == "issue_detected", (
        f"[{test_id}] Should detect '{error_word}'"
    )
    span_texts = {s["text"] for s in body.get("spans", [])}
    assert error_word in span_texts, (
        f"[{test_id}] Missing span for '{error_word}'"
    )
    if expected_correction:
        span = next(s for s in body["spans"] if s["text"] == error_word)
        sugg_texts = {s["text"].lower() for s in span.get("suggestions", [])}
        assert expected_correction.lower() in sugg_texts, (
            f"[{test_id}] Missing correction '{expected_correction}'"
        )
