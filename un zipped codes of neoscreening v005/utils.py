"""
Utility helpers for NeoScreenBot.
WHY: Keep presentational helpers isolated from core logic for clarity & reuse.
WHAT: Small HTML helpers for headers/badges.
"""
def case_header(case_id, mother_name, age_days, ga_weeks, birth_weight_g):
    case = (case_id.strip() if case_id else "—")
    name = (mother_name.strip() if mother_name else "—")
    return (
        f"""<div style='background:#f7f7f9;border:1px solid #eee;padding:12px;border-radius:10px;'>
<b>Case</b> — ID: <b>{case}</b> | Mother: <b>{name}</b> | 
Age: <b>{age_days} d</b> | GA: <b>{ga_weeks} w</b> | Birth weight: <b>{birth_weight_g} g</b>
</div>"""
    )

def badge(status):
    mapping = {
        "normal": ("✅ Normal", "#e6ffed", "#22863a"),
        "repeat": ("🟡 Repeat", "#fff5b1", "#735c0f"),
        "confirm": ("🟠 Confirm", "#ffe8cc", "#8b3f00"),
        "urgent": ("🔴 Urgent", "#ffeef0", "#b31d28"),
        "info": ("ℹ️ Info", "#f1f8ff", "#0366d6"),
    }
    label, bg, fg = mapping.get(status, ("ℹ️ Info", "#f1f8ff", "#0366d6"))
    return f"""<div style='background:{bg};color:{fg};padding:6px 10px;border-radius:999px;display:inline-block;'>
{label}
</div>"""
