"""
Core logic for interpreting CH and PKU screening results.
WHY: Centralize decision rules to avoid UI hardcoding and reduce errors.
WHAT: Each evaluator returns dict(status, message, followup?).
"""
def evaluate_ch(tsh, age_days, flags, rules):
    t = rules["CH"]["thresholds"]
    msg = rules["CH"]["messages"]
    status = "info"
    message = ""
    followup = None

    if tsh < t["exit_if_tsh_lt"]:
        status = "normal"; message = msg["normal"]
    elif t["repeat_low"] <= tsh <= t["repeat_high"]:
        status = "repeat"; message = msg["repeat"]
    elif t["serum_low"] <= tsh <= t["serum_high"]:
        status = "confirm"; message = msg["serum"]
    elif tsh >= t["urgent_if_tsh_ge"]:
        status = "urgent"; message = msg["urgent"]
    else:
        message = "⚠️ Undefined range. Please review rules.json."

    s = rules["shared"]["sampling_days"]
    if age_days < s["recommended_min"]:
        followup = f"Sampling before day {s['recommended_min']} — consider repeating at days {s['recommended_min']}-{s['recommended_max']}."
    elif age_days > s["window_max"]:
        followup = f"Sampling after day {s['window_max']} — ensure clinical correlation and consider repeat."

    return {"status": status, "message": message, "followup": followup}

def evaluate_pku(phe, stage, age_days, flags, rules):
    """
    Parameters
    ----------
    phe : float
        If stage == 'DBS', this is DBS Phe; if 'HPLC', this is confirmatory HPLC Phe.
    stage : str
        'DBS' or 'HPLC' — controls which branch of rules is applied.
    """
    status = "info"
    message = ""
    followup = None

    if stage == "DBS":
        dbs_thr = rules["PKU"]["dbs_threshold"]
        msgs = rules["PKU"]["messages"]
        if phe < dbs_thr:
            status = "normal"; message = msgs["dbs_normal"]
        else:
            status = "confirm"; message = msgs["dbs_to_hplc"]
    else:  # HPLC
        thr = rules["PKU"]["hplc_thresholds"]
        msgs = rules["PKU"]["hplc_messages"]
        if phe >= thr["treat_if_ge"]:
            status = "urgent"; message = msgs["treat"]
        elif thr["repeat_low"] <= phe <= thr["repeat_high"]:
            status = "repeat"; message = msgs["repeat"]
        elif thr["observe_low"] <= phe <= thr["observe_high"]:
            status = "confirm"; message = msgs["observe"]
        else:
            status = "info"; message = "Value outside configured HPLC ranges. Check rules.json."

    s = rules["shared"]["sampling_days"]
    if age_days < s["recommended_min"]:
        followup = f"Sampling before day {s['recommended_min']} — consider repeating at days {s['recommended_min']}-{s['recommended_max']}."
    elif age_days > s["window_max"]:
        followup = f"Sampling after day {s['window_max']} — ensure clinical correlation and consider repeat."

    return {"status": status, "message": message, "followup": followup}

def build_notes(flags, rules, program):
    notes = []
    sc = rules[program].get("special_cases", {})
    shared_sc = rules.get("shared", {}).get("special_cases", {})

    if flags.get("preterm"):
        notes.append(sc.get("preterm", shared_sc.get("preterm", "Preterm infant: follow scheduled rescreening.")))
    if flags.get("vlbw"):
        notes.append(sc.get("vlbw", shared_sc.get("vlbw", "VLBW infant: rescreening is required.")))
    elif flags.get("lbw"):
        notes.append(sc.get("lbw", shared_sc.get("lbw", "LBW infant: rescreening is recommended.")))
    if flags.get("macrosomia"):
        notes.append(sc.get("macrosomia", shared_sc.get("macrosomia", "Macrosomic infant: consider rescreening.")))

    if flags.get("nicu"):
        notes.append(sc.get("nicu", shared_sc.get("nicu", "NICU admission: scheduled rescreening required.")))
    if flags.get("transfusion"):
        notes.append(sc.get("transfusion", shared_sc.get("transfusion", "Recent transfusion: rescreen 48–72h post-transfusion.")))
    if flags.get("meds"):
        notes.append(sc.get("drugs", shared_sc.get("drugs", "Interfering medications: rescreen per protocol.")))
    if flags.get("dialysis") and program == "PKU":
        notes.append(sc.get("dialysis", shared_sc.get("dialysis", "Dialysis: rescreen 48–72h post-procedure.")))

    return notes
