"""
Structural OCR error detection integration tests.

Categories:
  1. Character confusions  — hand-written coherent sentences
  3. Multi-error texts
  4. Hard / tricky cases

Every sentence in this file is hand-written to read naturally, with
the corrupted word playing its proper grammatical role.  An LLM
next-token predictor needs real context (not ad-lib templates with a
slot for any word) to score whether a candidate correction fits.
"""

import pytest
from helpers import ocr_check


# ═══════════════════════════════════════════════════════════════════════
# 1. CHARACTER CONFUSIONS
# ═══════════════════════════════════════════════════════════════════════

# ── 1a. rn → m  confusion ─────────────────────────────────────────────
# Two adjacent letters "rn" look like "m" in many OCR fonts, so the
# engine often outputs "rn" where the printed text said "m".

CHAR_RN_M_CASES = [
    ("The federal governrnent announced sweeping tariff changes late Friday.",
        "governrnent", "government", "rn_m_government_1"),
    ("Citizens expect the governrnent to disclose its findings promptly.",
        "governrnent", "government", "rn_m_government_2"),
    ("She answered the question in a brusque rnanner that ended the conversation.",
        "rnanner", "manner", "rn_m_manner_1"),
    ("The bakery opens early every rnorning except Sunday.",
        "rnorning", "morning", "rn_m_morning_1"),
    ("We spent the whole surnrner at my grandmother's house on the lake.",
        "surnrner", "summer", "rn_m_summer_1"),
    ("The captain gave a curt cornrnand and the crew sprang into action.",
        "cornrnand", "command", "rn_m_command_1"),
    ("The cornrnercial break lasted nearly four minutes.",
        "cornrnercial", "commercial", "rn_m_commercial_1"),
    ("His cornrnitrnent to the project was evident in his long hours.",
        "cornrnitrnent", "commitment", "rn_m_commitment_1"),
    ("The flu is a cornrnon illness at this time of year.",
        "cornrnon", "common", "rn_m_common_1"),
    ("Local cornrnunity groups organized the annual food drive.",
        "cornrnunity", "community", "rn_m_community_1"),
    ("She posted a thoughtful cornrnent on the editorial about housing.",
        "cornrnent", "comment", "rn_m_comment_1"),
    ("Clear cornrnunication is essential during any emergency.",
        "cornrnunication", "communication", "rn_m_communication_1"),
    ("The electoral cornrnission verified the vote tallies overnight.",
        "cornrnission", "commission", "rn_m_commission_1"),
    ("I would recornrnend the tasting menu over the regular carte.",
        "recornrnend", "recommend", "rn_m_recommend_1"),
    ("Investigators will deterrnine the cause of the fire within days.",
        "deterrnine", "determine", "rn_m_determine_1"),
    ("The scar is a perrnanent reminder of the accident.",
        "perrnanent", "permanent", "rn_m_permanent_1"),
    ("The chess tournarnent drew grandmasters from twelve countries.",
        "tournarnent", "tournament", "rn_m_tournament_1"),
    ("Human activity continues to alter the global environrnent.",
        "environrnent", "environment", "rn_m_environment_1"),
    ("She transferred to the finance departrnent last quarter.",
        "departrnent", "department", "rn_m_department_1"),
    ("The developrnent of the vaccine took less than a year.",
        "developrnent", "development", "rn_m_development_1"),
    ("Trust is the fundarnental basis of any lasting friendship.",
        "fundarnental", "fundamental", "rn_m_fundamental_1"),
    ("The surgeon requested a sharper instrurnent from the tray.",
        "instrurnent", "instrument", "rn_m_instrument_1"),
    ("The civil war monurnent was unveiled after a long restoration.",
        "monurnent", "monument", "rn_m_monument_1"),
    ("At that rnoment the phone finally rang.",
        "rnoment", "moment", "rn_m_moment_1"),
    ("Her body temperature returned to norrnal by morning.",
        "norrnal", "normal", "rn_m_normal_1"),
    ("A frightened anirnai bolted across the road and disappeared into the brush.",
        "anirnai", "animal", "rn_m_animal_1"),
    ("The crirninal case was dismissed for lack of evidence.",
        "crirninal", "criminal", "rn_m_criminal_1"),
    ("The dosage required only a rninirnal adjustment after the lab results.",
        "rninirnal", "minimal", "rn_m_minimal_1"),
    ("The patient is in the terrninal ward under hospice care.",
        "terrninal", "terminal", "rn_m_terminal_1"),
    ("She sent a forrnal complaint to the licensing board.",
        "forrnal", "formal", "rn_m_formal_1"),
    ("The ordeal left him in a fragile rnental state.",
        "rnental", "mental", "rn_m_mental_1"),
    ("The dentist recommended the rernoval of all four wisdom teeth.",
        "rernoval", "removal", "rn_m_removal_1"),
    ("The factory orders raw rnaterial from a single supplier.",
        "rnaterial", "material", "rn_m_material_1"),
    ("Quartz is a common rnineral in granite and sandstone.",
        "rnineral", "mineral", "rn_m_mineral_1"),
    ("The therrnal blanket kept the climbers alive through the night.",
        "therrnal", "thermal", "rn_m_thermal_1"),
    ("The war rnernorial lists every soldier from the county who never returned.",
        "rnernorial", "memorial", "rn_m_memorial_1"),
    ("The nurnerical answer is less interesting than the method.",
        "nurnerical", "numerical", "rn_m_numerical_1"),
    ("The experirnental drug showed promising results in early trials.",
        "experirnental", "experimental", "rn_m_experimental_1"),
    ("Hydrogen is the simplest elernent on the periodic table.",
        "elernent", "element", "rn_m_element_1"),
]


# ── 1b. cl → d  confusion ─────────────────────────────────────────────
# The letters "cl" together can be misread as "d" in dense fonts.

CHAR_CL_D_CASES = [
    ("The new regulations indude stricter penalties for repeat offenders.",
        "indude", "include", "cl_d_include_1"),
    ("The senator wanted to dedare her position on the bill before the recess.",
        "dedare", "declare", "cl_d_declare_1"),
    ("The airline decided to exdude pets from its busiest flights.",
        "exdude", "exclude", "cl_d_exclude_1"),
    ("The jury could not condude its deliberations before the weekend.",
        "condude", "conclude", "cl_d_conclude_1"),
    ("The veterans filed a request to redaim their unpaid benefits.",
        "redaim", "reclaim", "cl_d_reclaim_1"),
    ("Sales began to dedine in the second half of the fiscal year.",
        "dedine", "decline", "cl_d_decline_1"),
    ("The court ordered the company to disdose its internal emails.",
        "disdose", "disclose", "cl_d_disclose_1"),
    ("Please endose a self-addressed envelope with your application.",
        "endose", "enclose", "cl_d_enclose_1"),
    ("The king used the royal herald to prodaim the new law.",
        "prodaim", "proclaim", "cl_d_proclaim_1"),
    ("Critics were quick to adaim her debut novel as a masterpiece.",
        "adaim", "acclaim", "cl_d_acclaim_1"),
    ("Cooler temperatures tend to indine people toward heartier meals.",
        "indine", "incline", "cl_d_incline_1"),
    ("The reduse poet refused all interview requests for forty years.",
        "reduse", "recluse", "cl_d_recluse_1"),
    ("The nudear reactor was shut down for scheduled maintenance.",
        "nudear", "nuclear", "cl_d_nuclear_1"),
    ("The cirdular saw is stored on the workbench against the far wall.",
        "cirdular", "circular", "cl_d_circular_1"),
    ("There are no partidular requirements for this introductory course.",
        "partidular", "particular", "cl_d_particular_1"),
    ("The fireworks display was truly spectadular that year.",
        "spectadular", "spectacular", "cl_d_spectacular_1"),
    ("The moledular structure of the compound was mapped over three months.",
        "moledular", "molecular", "cl_d_molecular_1"),
    ("Recovery will require several weeks of musdular rehabilitation.",
        "musdular", "muscular", "cl_d_muscular_1"),
    ("The sedular university requires no religious affiliation from students.",
        "sedular", "secular", "cl_d_secular_1"),
    ("She read a fascinating artide about the history of the lighthouse.",
        "artide", "article", "cl_d_article_1"),
    ("The delivery vehicde was waiting at the loading dock.",
        "vehicde", "vehicle", "cl_d_vehicle_1"),
    ("His recovery was nothing short of a mirade.",
        "mirade", "miracle", "cl_d_miracle_1"),
    ("The biggest obstade to reform is public apathy.",
        "obstade", "obstacle", "cl_d_obstacle_1"),
    ("The monks kept a careful chronide of every important event.",
        "chronide", "chronicle", "cl_d_chronicle_1"),
    ("The octopus extended a single tentade toward the diver's camera.",
        "tentade", "tentacle", "cl_d_tentacle_1"),
    ("The priestess delivered the orade's cryptic message to the king.",
        "orade", "oracle", "cl_d_oracle_1"),
    ("The aurora was a spectade that drew tourists to the far north.",
        "spectade", "spectacle", "cl_d_spectacle_1"),
    ("Each dust partide glittered in the shaft of afternoon light.",
        "partide", "particle", "cl_d_particle_1"),
]


# ── 1c. vv → w  confusion ─────────────────────────────────────────────
# Two adjacent "v" shapes are commonly misread as "w".

CHAR_VV_W_CASES = [
    ("The povver plant supplies electricity to the entire valley.",
        "povver", "power", "vv_w_power_1"),
    ("The bell tovver was restored using funds from a private donor.",
        "tovver", "tower", "vv_w_tower_1"),
    ("The river level was lovver than usual for this time of year.",
        "lovver", "lower", "vv_w_lower_1"),
    ("A single yellow flovver grew beside the neglected path.",
        "flovver", "flower", "vv_w_flower_1"),
    ("She took a quick shovver before the guests arrived.",
        "shovver", "shower", "vv_w_shower_1"),
    ("Hovvever, most of the evidence pointed in a different direction.",
        "Hovvever", "However", "vv_w_however_1"),
    ("The ovvner of the bookshop greeted every regular by name.",
        "ovvner", "owner", "vv_w_owner_1"),
    ("The old mining tovvn is nearly abandoned today.",
        "tovvn", "town", "vv_w_town_1"),
    ("She pulled on a pair of soft brovvn boots before stepping outside.",
        "brovvn", "brown", "vv_w_brown_1"),
    ("The crovvn of thorns pierced the statue's forehead in painful relief.",
        "crovvn", "crown", "vv_w_crown_1"),
    ("The sun was going dovvn as the ferry pulled into the harbor.",
        "dovvn", "down", "vv_w_down_1"),
    ("He almost let himself drovvn in self-pity after the diagnosis.",
        "drovvn", "drown", "vv_w_drown_1"),
    ("The frovvn on her face made clear that dinner had not gone well.",
        "frovvn", "frown", "vv_w_frown_1"),
    ("The puppy had grovvn into a lanky, awkward adolescent by September.",
        "grovvn", "grown", "vv_w_grown_1"),
    ("The poet is vvidely knovvn for her early collection on grief.",
        "knovvn", "known", "vv_w_known_1"),
    ("Every option has been shovvn to involve some measure of risk.",
        "shovvn", "shown", "vv_w_shown_1"),
    ("The baseball was throvvn over the fence and into the neighbor's yard.",
        "throvvn", "thrown", "vv_w_thrown_1"),
    ("Someone had left the vvindow open all night and the carpet was soaked.",
        "vvindow", "window", "vv_w_window_1"),
    ("The coldest vvinter in a decade killed off the citrus orchards.",
        "vvinter", "winter", "vv_w_winter_1"),
    ("The villagers spoke of her wisdom as a gift from her late grandmother.",
        "vvisdom", "wisdom", "vv_w_wisdom_1"),
]


# ── 1e. fi  ligature garble  ──────────────────────────────────────────
# The "fi" ligature often scans as "ft" or "fm" when OCR misreads the
# combined glyph.

CHAR_FI_CASES = [
    ("Please let me know if you fmd my lost keys in the lobby.",
        "fmd", "find", "fi_find_1"),
    ("The ftre had been smoldering in the attic for hours before anyone noticed.",
        "ftre", "fire", "fi_fire_1"),
    ("The heron speared a ftsh and flew back to its nest.",
        "ftsh", "fish", "fi_fish_1"),
    ("Please ftll the kettle before you start the coffee.",
        "ftll", "fill", "fi_fill_1"),
    ("The documentary ftlm covers the 1968 Olympic protests in detail.",
        "ftlm", "film", "fi_film_1"),
    ("The ftnal exam is scheduled for the Friday after Thanksgiving.",
        "ftnal", "final", "fi_final_1"),
    ("The CFO presented the department's ftnance plan to the board.",
        "ftnance", "finance", "fi_finance_1"),
    ("She broke a ftnger playing softball last weekend.",
        "ftnger", "finger", "fi_finger_1"),
    ("The old family ftrm had been in business for almost a century.",
        "ftrm", "firm", "fi_firm_1"),
    ("The ftrst train leaves the station at five fifty-two in the morning.",
        "ftrst", "first", "fi_first_1"),
    ("He counted to ftve before opening his eyes.",
        "ftve", "five", "fi_five_1"),
    ("The cows had grazed the fteld completely bare by August.",
        "fteld", "field", "fi_field_1"),
    ("The boxer's last ftght ended in a tenth-round knockout.",
        "ftght", "fight", "fi_fight_1"),
    ("The ftgure in the painting has never been identified by historians.",
        "ftgure", "figure", "fi_figure_1"),
    ("Please place the ftle in the top drawer of the cabinet.",
        "ftle", "file", "fi_file_1"),
    ("The water ftlter should be replaced every three months.",
        "ftlter", "filter", "fi_filter_1"),
    ("That is a ftne proposal, but we cannot afford it this year.",
        "ftne", "fine", "fi_fine_1"),
    ("Her fttness routine includes an hour of swimming every morning.",
        "fttness", "fitness", "fi_fitness_1"),
    ("The deadline is ftxed and cannot be extended under any circumstances.",
        "ftxed", "fixed", "fi_fixed_1"),
]


# ── 1f. miscellaneous m → rn and related confusions ───────────────────
# Where a printed "m" is output as "rn" or other similar smears.

CHAR_MISC_CASES = [
    ("Every hurnan being is entitled to basic dignity and respect.",
        "hurnan", "human", "misc_human_1"),
    ("The bread will rise faster if you keep the dough in a warrn corner of the kitchen.",
        "warrn", "warm", "misc_warm_1"),
    ("The storm did no serious harrn to the orchard despite high winds.",
        "harrn", "harm", "misc_harm_1"),
    ("The fire alarrn rang through every floor of the dormitory.",
        "alarrn", "alarm", "misc_alarm_1"),
    ("The old inn had a certain rustic charrn that the new hotel lacked.",
        "charrn", "charm", "misc_charm_1"),
    ("My uncle grew up on a dairy farrn near the Canadian border.",
        "farrn", "farm", "misc_farm_1"),
    ("A tropical storrn was forecast to make landfall by Thursday.",
        "storrn", "storm", "misc_storm_1"),
    ("The new chancellor promised to reforrn the admissions process.",
        "reforrn", "reform", "misc_reform_1"),
    ("The software runs on every major platforrn without modification.",
        "platforrn", "platform", "misc_platform_1"),
    ("Each student must wear the school uniforrn to the assembly.",
        "uniforrn", "uniform", "misc_uniform_1"),
    ("The planning board hopes to transforrn the abandoned lot into a park.",
        "transforrn", "transform", "misc_transform_1"),
    ("The band will perforrn twice on opening night.",
        "perforrn", "perform", "misc_perform_1"),
    ("Please inforrn the front desk if you need an extra pillow.",
        "inforrn", "inform", "misc_inform_1"),
    ("The gardener pulled a worrn from the freshly turned soil.",
        "worrn", "worm", "misc_worm_1"),
    ("The shift of power broke every diplomatic norrn established since the war.",
        "norrn", "norm", "misc_norm_1"),
    ("You need to fill out a separate forrn for each dependent.",
        "forrn", "form", "misc_form_1"),
]


# ── Combined character-confusion cases ────────────────────────────────

CHAR_CONFUSION_CASES = (
    CHAR_RN_M_CASES
    + CHAR_CL_D_CASES
    + CHAR_VV_W_CASES
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
# 3. MULTIPLE ERRORS PER TEXT
# ═══════════════════════════════════════════════════════════════════════

MULTI_ERROR_CASES = [
    # ── base 1 ──
    ("The government policy was reviewed by the cornrnittee", 1, "multi_1a"),
    ("The governrnent policy was revievved by the committee", 1, "multi_1b"),
    ("The governrnent policy was revievved by the cornrnittee", 2, "multi_1d"),
    # ── base 2 ──
    ("The departrment issued a new policy docurnent", 1, "multi_2a"),
    ("The departrment issuecl a nevv policy document", 1, "multi_2b"),
    ("The department issued a nevv policy docurnent", 1, "multi_2c"),
    ("The departrment issued a nevv policy docurnent", 1, "multi_2d"),
    # ── base 3 ──
    ("The environrnent needs irnrnediate protection from pollution", 1, "multi_3a"),
    ("The environment needs immediate protection frorn pollution", 1, "multi_3b"),
    ("The environrnent needs irnrnediate protection from pollution", 1, "multi_3c"),
    ("The environrnent needs irnrnediate protection frorn pollution", 1, "multi_3d"),
    # ── base 4 ──
    ("Citizens should exarnine the official report carefully", 1, "multi_4a"),
    ("Citizens should exarnine the official report carefully", 1, "multi_4b"),
    ("Citizens should exarnine the official report carefully", 1, "multi_4d"),
    # ── base 5 ──
    ("The developrnent of the cornrnunity was a rnajor priority", 2, "multi_5a"),
    ("The development of the cornrnunity was a major priority", 1, "multi_5b"),
    ("The developrnent of the community vvas a major priority", 1, "multi_5c"),
    ("The developrnent of the cornrnunity vvas a rnajor priority", 1, "multi_5d"),
    # ── base 6 ──
    ("The organization published its annual report yesterclay", 1, "multi_6c"),
    ("The organization published its annual report yesterclay", 1, "multi_6d"),
    # ── base 7 ──
    ("Researchers condudecl that the experirnent was a success", 2, "multi_7a"),
    ("Researchers concluded that the experirnent vvas a success", 1, "multi_7b"),
    ("Researchers condudecl that the experiment was a success", 1, "multi_7c"),
    ("Researchers condudecl that the experirnent vvas a success", 1, "multi_7d"),
    # ── base 8 ──
    ("The cornrnercial district was transforrned over the decade", 1, "multi_8a"),
    ("The cornrnercial district vvas transformed over the clecade", 2, "multi_8b"),
    ("The commercial clistrict was transforrned over the decade", 1, "multi_8c"),
    ("The cornrnercial clistrict vvas transforrned over the clecade", 2, "multi_8d"),
    # ── base 10 ──
    ("Local authorities confirmed the perrnanent closure", 1, "multi_10a"),
    ("Local authorities confirrned the perrnanent closure", 1, "multi_10b"),
    ("Local authorities confirrned the permanent closure", 1, "multi_10c"),
    ("Local authorities confirrned the perrnanent closure", 2, "multi_10d"),
    # ── base 11 ──
    ("The ftnal report indudecl several recornrnendations", 2, "multi_11a"),
    ("The final report included several recornrnendations", 1, "multi_11b"),
    ("The ftnal report included several recommendations", 1, "multi_11c"),
    ("The ftnal report indudecl several recornrnendations", 1, "multi_11d"),
    # ── base 12 ──
    ("The instrurnent was usecl for rneasuring ternperature", 2, "multi_12a"),
    ("The instrument vvas used for measuring ternperature", 1, "multi_12b"),
    ("The instrurnent was used for measuring temperature", 1, "multi_12c"),
    ("The instrurnent vvas usecl for rneasuring ternperature", 1, "multi_12d"),
    # ── base 13 ──
    ("The cornrnittee examinecl the proposed arnendment", 1, "multi_13a"),
    ("The cornrnittee examined the proposed arnendrnent", 1, "multi_13b"),
    ("The committee exarnined the proposed amendment", 1, "multi_13c"),
    ("The cornrnittee examinecl the proposed arnendrnent", 1, "multi_13d"),
    # ── base 14 ──
    ("The governrnent announced a fundarnental reforrn plan", 1, "multi_14a"),
    ("The governrnent announcecl a fundamental reforrn plan", 2, "multi_14b"),
    ("The government announced a fundarnental reform plan", 1, "multi_14c"),
    ("The governrnent announcecl a fundarnental reforrn plan", 2, "multi_14d"),
    # ── base 15 ──
    ("The experirnental platforrn was deployecl last rnonth", 2, "multi_15a"),
    ("The experimental platform vvas deployed last month", 1, "multi_15b"),
    ("The experirnental platform was deployed last rnonth", 1, "multi_15c"),
    ("The experirnental platforrn vvas deployecl last rnonth", 2, "multi_15d"),
    # ── base 16 ──
    ("Students should cornplete the assignrnent by Friday", 1, "multi_16a"),
    ("Stuclents should complete the assignrnent by Friclay", 2, "multi_16b"),
    ("Stuclents should cornplete the assignrnent by Friclay", 2, "multi_16d"),
    # ── base 17 ──
    ("The police departrment announced new safety rneasures", 1, "multi_17a"),
    ("The police department announced nevv safety measures", 1, "multi_17b"),
    ("The police departrment announced new safety rneasures", 1, "multi_17c"),
    ("The police departrment announced nevv safety rneasures", 1, "multi_17d"),
    # ── base 18 ──
    ("The nurnerical analysis producecl unexpected results", 2, "multi_18a"),
    ("The nurnerical analysis producecl unexpected results", 1, "multi_18c"),
    ("The nurnerical analysis producecl unexpected results", 1, "multi_18d"),
    # ── base 19 ──
    ("Residents dernanded irnrnediate action frorn the council", 2, "multi_19a"),
    ("Residents demanded irnrnediate action from the council", 1, "multi_19b"),
    ("Residents dernanded immediate action frorn the council", 1, "multi_19c"),
    ("Residents dernanded irnrnediate action frorn the council", 1, "multi_19d"),
    # ── base 20 ──
    ("The articde described the spectadular transforrnation", 2, "multi_20a"),
    ("The article described the spectadular transformation", 1, "multi_20b"),
    ("The artide clescribed the spectacular transforrnation", 2, "multi_20c"),
    ("The articde clescribed the spectadular transforrnation", 2, "multi_20d"),
    # ── base 21 ──
    ("The crirninal was apprehendecl near the tovvn center", 2, "multi_21a"),
    ("The criminal was apprehended near the tovvn center", 1, "multi_21b"),
    ("The crirninal vvas apprehended near the town center", 2, "multi_21c"),
    ("The crirninal vvas apprehendecl near the tovvn center", 2, "multi_21d"),
    # ── base 22 ──
    ("The rnedical facility requirecl additional equiprnent", 2, "multi_22a"),
    ("The rnedical facility requirecl additional equiprnent", 1, "multi_22d"),
    # ── base 23 ──
    ("Parents should rnonitor their children's activities", 1, "multi_23a"),
    ("Parents should rnonitor their children's activities", 1, "multi_23d"),
    # ── base 24 ──
    ("The terrninal was closecl for rnaintenance last week", 2, "multi_24a"),
    ("The terminal was closed for rnaintenance last week", 1, "multi_24b"),
    ("The terrninal vvas closed for maintenance last vveek", 2, "multi_24c"),
    ("The terrninal vvas closecl for rnaintenance last vveek", 2, "multi_24d"),
    # ── base 25 ──
    ("The vehicde's perrnanent registration was approvecl", 2, "multi_25a"),
    ("The vehicde's perrnanent registration was approved", 1, "multi_25c"),
    ("The vehicde's perrnanent registration vvas approvecl", 1, "multi_25d"),
    # ── base 26 ──
    ("The comrnission released a preliminary report today", 1, "multi_26a"),
    ("The cornrnission released a prelirninary report toclay", 2, "multi_26b"),
    ("The cornrnission released a prelirninary report toclay", 1, "multi_26d"),
    # ── base 27 ──
    ("The moledular structure was analyzecl in the lab", 1, "multi_27a"),
    ("The moledular structure vvas analyzed in the lab", 2, "multi_27b"),
    ("The moledular structure vvas analyzecl in the lab", 2, "multi_27d"),
    # ── base 28 ──
    ("The rnineral deposits were discoveredl last year", 1, "multi_28a"),
    ("The rnineral deposits vvere discovered last year", 2, "multi_28c"),
    ("The rnineral deposits vvere discoveredl last year", 1, "multi_28d"),
    # ── base 29 ──
    ("Workers dernanded that the uniforrn policy be changed", 2, "multi_29a"),
    ("Vvorkers demanded that the uniforrn policy be changed", 1, "multi_29b"),
    ("Workers dernanded that the uniform policy be changecl", 1, "multi_29c"),
    ("Vvorkers dernanded that the uniforrn policy be changecl", 2, "multi_29d"),
    # ── base 30 ──
    ("The alarnm system was testecl during the storm", 2, "multi_30a"),
    ("The alarm systern was tested during the storm", 1, "multi_30b"),
    ("The alarrn system vvas tested during the storrn", 2, "multi_30c"),
    ("The alarrn systern vvas testecl during the storrn", 1, "multi_30d"),
    # ── base 31 ──
    ("The platforrn supportecl thousands of daily users", 2, "multi_31a"),
    ("The platforrn supported thousands of daily users", 1, "multi_31c"),
    ("The platforrn supported thousands of daily users", 1, "multi_31d"),
    # ── base 32 ──
    ("The rnuseum displayed a spectadular collection", 2, "multi_32a"),
    ("The rnuseum displayed a spectadular collection", 1, "multi_32c"),
    ("The rnuseum displayed a spectadular collection", 1, "multi_32d"),
    # ── base 33 ──
    ("Participants should cornplete the registration forrn", 1, "multi_33a"),
    ("Participants should cornplete the registration forrn", 1, "multi_33d"),
    # ── base 34 ──
    ("The education systern needs fundarnental changes", 1, "multi_34a"),
    ("The education system needs fundarnental changecl", 1, "multi_34b"),  # noqa: E501
    ("The education systern needs fundamental changecl", 1, "multi_34c"),
    ("The education systern needs fundarnental changecl", 1, "multi_34d"),
    # ── base 35 ──
    ("The recornrnendation was acceptecl by the board", 2, "multi_35a"),
    ("The recommendation vvas accepted by the board", 1, "multi_35b"),
    ("The recornrnendation was accepted by the board", 1, "multi_35c"),
    ("The recornrnendation vvas acceptecl by the board", 1, "multi_35d"),
    # ── base 36 ──
    ("International cornrnunication irnproved significantly", 2, "multi_36a"),
    ("International cornrnunication improved significantly", 1, "multi_36c"),
    ("International cornrnunication irnproved significantly", 2, "multi_36d"),
    # ── base 37 ──
    ("The rnernorial was visitecl by thousands of tourists", 2, "multi_37a"),
    ("The memorial vvas visited by thousands of tourists", 1, "multi_37b"),
    ("The rnernorial was visited by thousands of tourists", 1, "multi_37c"),
    ("The rnernorial vvas visitecl by thousands of tourists", 1, "multi_37d"),
    # ── base 38 ──
    ("The ftnancial report indudecl quarterly earnings", 2, "multi_38a"),
    ("The ftnancial report included quarterly earnings", 1, "multi_38c"),
    ("The ftnancial report indudecl quarterly earnings", 1, "multi_38d"),
    # ── base 39 ──
    ("The national park attracted rnillions of visitors", 1, "multi_39a"),
    ("The national park attractecl millions of visitors", 1, "multi_39c"),
    ("The national park attractecl rnillions of visitors", 1, "multi_39d"),
    # ── base 40 ──
    ("Scientists perforrned experirnents in the laboratory", 2, "multi_40a"),
    ("The scientists performed experirnents in the lab", 1, "multi_40b"),
    ("Scientists perforrned experiments in the laboratory", 1, "multi_40c"),
    ("The scientists perforrned experirnents in the laboratory", 1, "multi_40d"),
    # ── base 41 ──
    ("The cornrnunity center hostecl a fundraising event", 2, "multi_41a"),
    ("The community center hosted a fundraising event", 1, "multi_41b"),
    ("The cornrnunity center hosted a funclraising event", 2, "multi_41c"),
    ("The cornrnunity center hostecl a funclraising event", 1, "multi_41d"),
    # ── base 42 ──
    ("The therrnal energy systern was highly efficient", 2, "multi_42a"),
    ("The thermal energy system vvas highly efficient", 1, "multi_42b"),
    ("The therrnal energy systern was highly efficient", 1, "multi_42c"),
    ("The therrnal energy systern vvas highly efficient", 2, "multi_42d"),
    # ── base 43 ──
    ("Management approvecl the budget for the new project", 1, "multi_43a"),
    ("Managernent approved the budget for the nevv project", 1, "multi_43b"),
    ("Management approvecl the budget for the nevv project", 1, "multi_43c"),
    ("Managernent approvecl the budget for the nevv project", 1, "multi_43d"),
    # ── base 44 ──
    ("The teacher explained the experirnental procedure", 1, "multi_44a"),
    ("The teacher explained the experirnental procedure", 1, "multi_44b"),
    ("The teacher explained the experirnental procedure", 1, "multi_44d"),
    # ── base 45 ──
    ("The sedular institution published new guidelines", 1, "multi_45a"),
    ("The sedular institution published nevv guidelines", 2, "multi_45c"),
    ("The sedular institution published nevv guidelines", 1, "multi_45d"),
    # ── base 46 ──
    ("The rnanager confirrned the schedule for the event", 1, "multi_46a"),
    ("The rnanager confirmed the schedule for the event", 1, "multi_46b"),
    ("The manager confirrned the schedule for the event", 1, "multi_46c"),
    ("The rnanager confirrned the schedule for the event", 1, "multi_46d"),
    # ── base 47 ──
    ("The hospital administration announcecl new policies", 1, "multi_47a"),
    ("The hospital administration announced nevv policies", 1, "multi_47b"),
    ("The hospital administration announced nevv policies", 1, "multi_47c"),
    ("The hospital administration announcecl nevv policies", 2, "multi_47d"),
    # ── base 48 ──
    ("Voters should exarnine each candidate's platform", 1, "multi_48a"),
    ("Voters should examine each canclidate's platform", 1, "multi_48b"),
    ("Voters should exarnine each candidate's platform", 1, "multi_48c"),
    ("Voters should exarnine each canclidate's platform", 1, "multi_48d"),
    # ── base 49 ──
    ("The docurnent was signecl by all participating parties", 2, "multi_49a"),
    ("The document vvas signed by all participating parties", 1, "multi_49b"),
    ("The docurnent was signed by all participating parties", 1, "multi_49c"),
    ("The docurnent vvas signecl by all participating parties", 1, "multi_49d"),
    # ── base 50 ──
    ("The anirnal shelter receivecl generous donations", 2, "multi_50a"),
    ("The anirnal shelter received generous donations", 1, "multi_50c"),
    ("The anirnal shelter receivecl generous donations", 1, "multi_50d"),
    # ── base 51 ──
    ("The rnilitary cornrnander issuecl new orders today", 2, "multi_51a"),
    ("The military commander issued nevv orders today", 1, "multi_51b"),
    ("The rnilitary commander issued new orclers today", 2, "multi_51c"),
    ("The rnilitary cornrnander issuecl nevv orclers today", 2, "multi_51d"),
    # ── base 52 ──
    ("The ftlm festival attractecl international attention", 2, "multi_52a"),
    ("The ftlm festival attracted international attention", 1, "multi_52c"),
    ("The ftlm festival attractecl international attention", 1, "multi_52d"),
    # ── base 53 ──
    ("The irnportant docurnent was filed vvith the court", 2, "multi_53a"),
    ("The irnportant document was filed with the court", 1, "multi_53c"),
    ("The irnportant docurnent was filed vvith the court", 1, "multi_53d"),
    # ── base 54 ──
    ("Traffic congestion increasecl during the surnrner months", 1, "multi_54a"),
    ("The traffic congestion increased during the surnrner months", 1, "multi_54b"),
    ("The traffic congestion increasecl during the surnrner months", 1, "multi_54d"),
    # ── base 55 ──
    ("The netvvork systern requirecl significant upgrades", 2, "multi_55a"),
    ("The netvvork systern required significant upgracles", 2, "multi_55c"),
    ("The netvvork systern requirecl significant upgracles", 1, "multi_55d"),
    # ── base 56 ──
    ("The corrununity gardlen provided fresh vegetables", 2, "multi_56a"),
    ("The community garden provicled fresh vegetables", 1, "multi_56b"),
    ("The corrununity garden proviclecl fresh vegetables", 2, "multi_56c"),
    ("The corrununity garden provicled fresh vegetables", 2, "multi_56d"),
    # ── base 57 ──
    ("Engineers redesignecl the therrnal protection systern", 2, "multi_57a"),
    ("Engineers redesignecl the thermal protection system", 1, "multi_57c"),
    ("The engineers redesignecl the therrnal protection systern", 1, "multi_57d"),
    # ── base 58 ──
    ("The rnedical tearn completed the surgical procedure", 1, "multi_58a"),
    ("The rnedical team cornpleted the surgical procedure", 2, "multi_58b"),
    ("The medical tearn completed the surgical procedure", 1, "multi_58c"),
    ("The rnedical tearn cornpleted the surgical procedure", 2, "multi_58d"),
    # ── base 59 ──
    ("Investigators reviewecl the crirninal's background", 2, "multi_59a"),
    ("Investigators reviewecl the criminal's backgrounld", 2, "multi_59c"),
    ("The investigators reviewecl the crirninal's background", 1, "multi_59d"),
    # ── base 60 ──
    ("The school district approvecl a new curriculum", 1, "multi_60a"),
    ("The school district approved a nevv curriculum", 1, "multi_60b"),
    ("The school district approvecl a nevv curriculum", 2, "multi_60d"),
    # ── base 61 ──
    ("The public library expandecl its digital collection", 1, "multi_61c"),
    ("The public library expandecl its digital collection", 1, "multi_61d"),
    # ── base 62 ──
    ("The transportation systern servecl millions of riders", 1, "multi_62a"),
    ("The transportation systern servecl millions of riders", 1, "multi_62d"),
    # ── base 63 ──
    ("The construction cornpany completed the tovver on tirne", 1, "multi_63a"),
    ("The construction cornpany cornpleted the tower on time", 2, "multi_63b"),
    ("The construction company completed the tovver on time", 1, "multi_63c"),
    ("The construction cornpany cornpleted the tovver on tirne", 2, "multi_63d"),
    # ── base 64 ──
    ("The forrnal investigation uncoverecl critical evidence", 2, "multi_64a"),
    ("The forrnal investigation uncovered critical evidence", 1, "multi_64c"),
    ("The forrnal investigation uncoverecl critical evidence", 1, "multi_64d"),
    # ── base 65 ──
    ("Several ernployees cornplained about the new policy", 2, "multi_65a"),
    ("Several ernployees complained about the nevv policy", 1, "multi_65c"),
    ("Several ernployees cornplained about the nevv policy", 1, "multi_65d"),
    # ── base 66 ──
    ("The judge dismissecl the case due to insufficient evidence", 1, "multi_66a"),
    ("The juclge dismissed the case due to insufficient eviclence", 1, "multi_66b"),
    ("The juclge dismissecl the case due to insufficient eviclence", 1, "multi_66d"),
    # ── base 67 ──
    ("The vvindow was brokecl during the severe storm", 2, "multi_67a"),
    ("The window vvas broken during the severe storrn", 1, "multi_67b"),
    ("The vvindow was broken during the severe storm", 1, "multi_67c"),
    ("The vvindow vvas brokecl during the severe storrn", 1, "multi_67d"),
    # ── base 68 ──
    ("The cornpany's annual revenue increasecl significantly", 1, "multi_68a"),
    ("The cornpany's annual revenue increased significantly", 1, "multi_68c"),
    ("The cornpany's annual revenue increasecl significantly", 1, "multi_68d"),
    # ── base 69 ──
    ("The rnusician perforrned a beautiful concert last night", 1, "multi_69a"),
    ("The rnusician performed a beautiful concert last night", 1, "multi_69c"),
    ("The rnusician perforrned a beautiful concert last night", 1, "multi_69d"),
    # ── base 70 ──
    ("The architect designed a spectadular building", 1, "multi_70a"),
    ("The architect clesigned a spectadular building", 1, "multi_70b"),
    ("The architect clesigned a spectadular building", 1, "multi_70d"),
    # ── base 71 ──
    ("The president announcecl a new trade agreernent", 1, "multi_71a"),
    ("The president announced a nevv trade agreement", 1, "multi_71b"),
    ("The president announced a new trade agreernent", 1, "multi_71c"),
    ("The president announcecl a nevv trade agreernent", 1, "multi_71d"),
    # ── base 72 ──
    ("The university publishecl its research ftndings", 1, "multi_72a"),
    ("The university publishecl its research ftndings", 1, "multi_72d"),
    # ── base 73 ──
    ("The environmental agency rnonitored the water quality", 1, "multi_73a"),
    ("The environmental agency rnonitored the water quality", 1, "multi_73d"),
    # ── base 74 ──
    ("The software developrnent tearn released a new version", 1, "multi_74a"),
    ("The software developrnent tearn released a nevv version", 1, "multi_74b"),
    ("The software development tearn released a new version", 1, "multi_74c"),
    ("The software developrnent tearn released a nevv version", 1, "multi_74d"),
    # ── base 75 ──
    ("The farrner harvested a rnajor crop this season", 2, "multi_75a"),
    ("The farmer harvested a major crop this season", 1, "multi_75b"),
    ("The farrner harvested a major crop this season", 1, "multi_75c"),
    ("The farrner harvested a rnajor crop this season", 1, "multi_75d"),
    # ── base 76 ──
    ("The factory producecl thousands of uniforrns daily", 2, "multi_76a"),
    ("The factory producecl thousands of uniforms daily", 1, "multi_76c"),
    ("The factory producecl thousands of uniforrns daily", 1, "multi_76d"),
    # ── base 77 ──
    ("The historian exarnined ancient docurnents carefully", 2, "multi_77a"),
    ("The historian examined ancient docurnents carefully", 1, "multi_77b"),
    ("The historian exarnined ancient documents carefully", 1, "multi_77c"),
    ("The historian exarnined ancient docurnents carefully", 2, "multi_77d"),
    # ── base 78 ──
    ("The clirnate scientists publishecl their findings", 1, "multi_78a"),
    ("The climate scientists published their ftndings", 1, "multi_78b"),
    ("The clirnate scientists publishecl their ftndings", 1, "multi_78d"),
    # ── base 79 ──
    ("The dernonstration attractecl international rnedia attention", 2, "multi_79a"),
    ("The dernonstration attracted international rnedia attention", 1, "multi_79c"),
    ("The dernonstration attractecl international rnedia attention", 1, "multi_79d"),
    # ── base 80 ──
    ("Engineers testecl the netvvork security protocol", 1, "multi_80a"),
    ("Engineers testecl the network security protocol", 1, "multi_80c"),
    ("The engineers testecl the netvvork security protocol", 1, "multi_80d"),
    # ── base 81 ──
    ("The hospital announcecl new visiting hours", 1, "multi_81a"),
    ("The hospital announced nevv visiting hours", 1, "multi_81b"),
    ("The hospital announcecl nevv visiting hours", 1, "multi_81d"),
    # ── base 82 ──
    ("The experirnental rnedicine showed prornising results", 2, "multi_82a"),
    ("The experimental medicine shovved promising results", 1, "multi_82b"),
    ("The experirnental medicine showed prornising results", 1, "multi_82c"),
    ("The experirnental rnedicine shovved prornising results", 2, "multi_82d"),
    # ── base 83 ──
    ("The library catalog contained rnillions of entries", 1, "multi_83a"),
    ("The library catalog containecl millions of entries", 1, "multi_83c"),
    ("The library catalog containecl rnillions of entries", 1, "multi_83d"),
    # ── base 84 ──
    ("The technology cornpany announcecl a merger", 1, "multi_84a"),
    ("The technology company announced a rnerger", 1, "multi_84b"),
    ("The technology company announced a rnerger", 1, "multi_84c"),
    ("The technology cornpany announcecl a rnerger", 1, "multi_84d"),
    # ── base 85 ──
    ("The volunteer organization helped thousands of farnilies", 1, "multi_85a"),
    ("The volunteer organization helped thousands of families", 1, "multi_85c"),
    ("The volunteer organization helped thousands of farnilies", 1, "multi_85d"),
    # ── base 86 ──
    ("The infrastrudure requirecl significant investrnent", 2, "multi_86a"),
    ("The infrastrudure required significant investrnent", 2, "multi_86c"),
    ("The infrastrudure requirecl significant investrnent", 1, "multi_86d"),
    # ── base 87 ──
    ("The professor explained the cornplex rnathematical concept", 1, "multi_87a"),
    ("The professor explained the cornplex rnathernatical concept", 2, "multi_87b"),
    ("The professor explained the cornplex rnathernatical concept", 1, "multi_87d"),
    # ── base 88 ──
    ("The election cornrnission verifiecl the results", 1, "multi_88a"),
    ("The election commission verifiecl the results", 1, "multi_88c"),
    ("The election cornrnission verifiecl the results", 1, "multi_88d"),
    # ── base 89 ──
    ("The rnuseum's collection indudecl rare artifacts", 1, "multi_89a"),
    ("The rnuseum's collection included rare artifacts", 1, "multi_89c"),
    ("The rnuseum's collection indudecl rare artifacts", 1, "multi_89d"),
    # ── base 90 ──
    ("The governrnent spokesperson issuecl a clarification", 1, "multi_90a"),
    ("The governrnent spokesperson issued a clarification", 1, "multi_90b"),
    ("The government spokesperson issued a darification", 1, "multi_90c"),
    ("The governrnent spokesperson issuecl a darification", 1, "multi_90d"),
    # ── base 91 ──
    ("The particular spectade drew considerable attention", 1, "multi_91a"),
    ("The particular spectacle drevv considerable attention", 1, "multi_91b"),
    ("The particular spectade drevv considerable attention", 1, "multi_91d"),
    # ── base 92 ──
    ("The diplornat addressecl the international conference", 1, "multi_92a"),
    ("The diplornat addressed the international conference", 1, "multi_92c"),
    ("The diplornat addressecl the international conference", 1, "multi_92d"),
    # ── base 93 ──
    ("The financial rnarket experiencecl unprecedented growth", 1, "multi_93a"),
    ("The financial market experienced unprecedented grovvth", 1, "multi_93b"),
    ("The financial rnarket experiencecl unprecedented grovvth", 1, "multi_93d"),
    # ── base 94 ──
    ("The governrnent fundecl the environmental research program", 1, "multi_94a"),
    ("The government funded the environrnental research program", 1, "multi_94b"),
    ("The government fundecl the environmental research program", 1, "multi_94c"),
    ("The governrnent fundecl the environrnental research program", 1, "multi_94d"),
    # ── base 95 ──
    ("The nurnerical data revealecl a significant trend", 2, "multi_95a"),
    ("The numerical clata revealed a significant trend", 1, "multi_95b"),
    ("The nurnerical data revealed a significant trend", 1, "multi_95c"),
    ("The nurnerical clata revealecl a significant trend", 1, "multi_95d"),
    # ── base 96 ──
    ("The cornpany launchled a new cornrnercial product", 2, "multi_96a"),
    ("The cornpany launched a nevv commercial product", 2, "multi_96c"),
    ("The cornpany launchled a nevv cornrnercial product", 1, "multi_96d"),
    # ── base 97 ──
    ("The dernonstrators rnarched through the tovvn peacefully", 2, "multi_97a"),
    ("The dernonstrators marched through the town peacefully", 1, "multi_97c"),
    ("The dernonstrators rnarched through the tovvn peacefully", 1, "multi_97d"),
    # ── base 98 ──
    ("The scholarship prograrn supportecl talented students", 1, "multi_98a"),
    ("The scholarship prograrn supported talented students", 1, "multi_98d"),
    # ── base 99 ──
    ("The reforrn proposal was debatecl in the legislature", 2, "multi_99a"),
    ("The reforrn proposal vvas debated in the legislature", 2, "multi_99c"),
    ("The reforrn proposal vvas debatecl in the legislature", 2, "multi_99d"),
    # ── base 100 ──
    ("The international cornrnission reviewecl trade policies", 1, "multi_100a"),
    ("The international commission revievved trade policies", 1, "multi_100b"),
    ("The international commission reviewed tracle policies", 1, "multi_100c"),
    ("The international cornrnission revievved tracle policies", 1, "multi_100d"),
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
# 4. HARD / TRICKY TRUE POSITIVES
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
    # ── Error that creates another valid word (wrong in context) ───────
    (
        "The police were called to the scene of the crirne",
        "crirne", "crime", "hard_realword_1",
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
    # ── Mixed bag: more tricky true positives ──────────────────────────
    # Valid rn→m OCR errors (m looks like rn in print)
    (
        "According to the acadernic journal the findings were inconclusive",
        "acadernic", "academic", "hard_misc_2",
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
        "The replacernent parts arrived within three business days",
        "replacernent", "replacement", "hard_misc_19",
    ),
    (
        "The investrnent portfolio was diversified across sectors",
        "investrnent", "investment", "hard_misc_21",
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
        "The achievernent was recognized by the international body",
        "achievernent", "achievement", "hard_misc_29",
    ),
    (
        "The improvernent in test scores delighted the teachers",
        "improvernent", "improvement", "hard_misc_30",
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
        "The attachrnent included the full financial breakdown",
        "attachrnent", "attachment", "hard_misc_38",
    ),
    (
        "The procurernent office handled all vendor contracts",
        "procurernent", "procurement", "hard_misc_39",
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
