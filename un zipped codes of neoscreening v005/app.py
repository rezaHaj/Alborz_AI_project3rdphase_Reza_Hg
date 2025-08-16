"""
Streamlit UI for NeoScreenBot (v0.0.5)
WHY: Centered, clean UI for non-specialists. One PKU field per stage (DBS/HPLC) with stage label (Stage 1/2).
"""
import io, json
import numpy as np
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

from logic import evaluate_ch, evaluate_pku, build_notes
from utils import case_header, badge

st.set_page_config(page_title="NeoScreenBot", page_icon="🍼", layout="centered")

# Load rules
@st.cache_data(show_spinner=False)
def load_rules():
    with open("rules.json", "r", encoding="utf-8") as f:
        return json.load(f)
RULES = load_rules()

st.title("🍼 NeoScreenBot")
st.caption("Decision-support for neonatal screening • CH & PKU • by **reza hg** (v0.0.5)")
st.info("⚠️ This tool supports decision-making and does not replace professional medical advice. No data is stored⚠️.")

# Sidebar nav
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["CH Screening", "PKU Screening", "Guide", "Show Rules", "About"])

def export_df(program, inputs, result, notes):
    row = {
        "program": program,
        "case_id": inputs.get("case_id",""),
        "mother_name": inputs.get("mother_name",""),
        "age_days": inputs.get("age_days", np.nan),
        "ga_weeks": inputs.get("ga_weeks", np.nan),
        "birth_weight_g": inputs.get("birth_weight_g", np.nan),
        "value_type": inputs.get("value_type",""),
        "value": inputs.get("value", np.nan),
        "units": inputs.get("units",""),
        "status": result.get("status",""),
        "message": result.get("message",""),
        "followup": result.get("followup",""),
        "notes": "; ".join(notes) if notes else ""
    }
    return pd.DataFrame([row])

def pdf_bytes(program, df: pd.DataFrame):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    x = 2*cm
    y = height - 2*cm
    def writeln(text, size=11, dy=14):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(x, y, str(text))
        y -= dy
    writeln(f"NeoScreenBot — {program} summary", size=14, dy=18)
    for col in df.columns:
        val = df.iloc[0][col]
        writeln(f"{col}: {val}")
    c.showPage(); c.save(); buf.seek(0)
    return buf

# Centered wrapper
def centered_container():
    left, mid, right = st.columns([1, 2, 1])
    return mid

with centered_container():
    with st.expander("Patient information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            case_id = st.text_input("Case ID (tracking code)")
            mother_name = st.text_input("Mother's name")
        with col2:
            age_days = st.number_input("Newborn age (days)", min_value=0, max_value=60, step=1, help="Recommended initial sampling: days 3–5")
            ga_weeks = st.number_input("Gestational age (weeks)", min_value=20, max_value=45, value=38, step=1)
        birth_weight_g = st.number_input("Birth weight (g)", min_value=400, max_value=7000, value=3200, step=50)
        st.markdown(case_header(case_id, mother_name, age_days, ga_weeks, birth_weight_g), unsafe_allow_html=True)

    with st.expander("Special conditions (optional)"):
        c1, c2, c3, c4 = st.columns(4)
        with c1: nicu = st.checkbox("NICU admission")
        with c2: transfusion = st.checkbox("Recent transfusion (72h)")
        with c3: meds = st.checkbox("Interfering meds")
        with c4: dialysis = st.checkbox("Dialysis (PKU)")

    flags = {
        "nicu": nicu, "transfusion": transfusion, "meds": meds, "dialysis": dialysis,
        "preterm": ga_weeks < RULES["shared"]["gestational_age"]["term_min_weeks"],
        "lbw": birth_weight_g < RULES["shared"]["birth_weight"]["lbw_g"],
        "vlbw": birth_weight_g < RULES["shared"]["birth_weight"]["vlbw_g"],
        "macrosomia": birth_weight_g > RULES["shared"]["birth_weight"]["macrosomia_g"],
    }

if page == "CH Screening":
    with centered_container():
        st.subheader("Congenital Hypothyroidism (CH)")
        tsh = st.number_input(f"TSH ({RULES['CH']['units']})", min_value=0.0, step=0.1, help="Unit: mU/L")
        if st.button("Evaluate CH", type="primary"):
            result = evaluate_ch(tsh=tsh, age_days=age_days, flags=flags, rules=RULES)
            st.markdown(badge(result["status"]), unsafe_allow_html=True)
            st.success(result["message"])
            if result.get("followup"): st.warning(result["followup"])
            notes = build_notes(flags, RULES, program="CH")
            if notes:
                st.markdown("**Notes / Context**")
                for n in notes: st.markdown(f"- {n}")
            inputs = dict(case_id=case_id, mother_name=mother_name, age_days=age_days,
                          ga_weeks=ga_weeks, birth_weight_g=birth_weight_g,
                          value_type="TSH", value=tsh, units=RULES["CH"]["units"])
            df = export_df("CH", inputs, result, notes)
            st.markdown("**Case summary (table)**"); st.dataframe(df, use_container_width=True)
            st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"),
                               file_name=f"{case_id or 'case'}_CH.csv", mime="text/csv")
            st.download_button("Download PDF", pdf_bytes("CH", df),
                               file_name=f"{case_id or 'case'}_CH.pdf", mime="application/pdf")

elif page == "PKU Screening":
    with centered_container():
        st.subheader("Phenylketonuria (PKU)")
        stage_label = st.radio("Select PKU stage", ["DBS (Stage 1)", "Confirmatory HPLC (Stage 2)"])
        if stage_label.startswith("DBS"):
            phe_value = st.number_input(f"DBS Phenylalanine ({RULES['PKU']['units']})", min_value=0.0, step=0.1, help="Unit: mg/dL")
            current_units = RULES["PKU"]["units"]; value_type = "DBS Phe"; stage = "DBS"
            st.caption("DBS screening (Stage 1) — if ≥ 4 mg/dL → do HPLC (no diet change).")
        else:
            phe_value = st.number_input(f"HPLC Phenylalanine ({RULES['PKU']['units']})", min_value=0.0, step=0.1, help="Unit: mg/dL")
            current_units = RULES["PKU"]["units"]; value_type = "HPLC Phe"; stage = "HPLC"
            st.caption("Confirmatory (Stage 2) — apply HPLC thresholds.")

        if st.button("Evaluate PKU", type="primary"):
            result = evaluate_pku(phe=phe_value, stage=stage, age_days=age_days, flags=flags, rules=RULES)
            st.markdown(badge(result["status"]), unsafe_allow_html=True)
            st.success(result["message"])
            if result.get("followup"): st.warning(result["followup"])
            notes = build_notes(flags, RULES, program="PKU")
            if notes:
                st.markdown("**Notes / Context**")
                for n in notes: st.markdown(f"- {n}")
            inputs = dict(case_id=case_id, mother_name=mother_name, age_days=age_days,
                          ga_weeks=ga_weeks, birth_weight_g=birth_weight_g,
                          value_type=value_type, value=phe_value, units=current_units)
            df = export_df("PKU", inputs, result, notes)
            st.markdown("**Case summary (table)**"); st.dataframe(df, use_container_width=True)
            st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"),
                               file_name=f"{case_id or 'case'}_PKU.csv", mime="text/csv")
            st.download_button("Download PDF", pdf_bytes("PKU", df),
                               file_name=f"{case_id or 'case'}_PKU.pdf", mime="application/pdf")

elif page == "Guide":
    with centered_container():
        st.subheader("📘 Screening Guide")
        try:
            with open("data/guide.md", "r", encoding="utf-8") as g:
                st.markdown(g.read())
        except FileNotFoundError:
            st.warning("Guide not found. Put your markdown in data/guide.md")

elif page == "Show Rules":
    with centered_container():
        st.subheader("Rules (JSON)")
        st.code(json.dumps(RULES, indent=2, ensure_ascii=False))
        st.caption("Edit rules.json to change thresholds/messages. Restart app to reload.")

elif page == "About":
    with centered_container():
        st.subheader("About NeoScreenBot")
        st.markdown("**Author:** reza hg | **Email:** reza.ai.developer@gmail.com")
        st.markdown("**Version:** 0.0.5")
        st.markdown("**Tech:** Python, Streamlit, JSON rules (no hardcoding), pandas/numpy, reportlab (PDF).")
        st.markdown("This app centers inputs on the page for better user experience.")
