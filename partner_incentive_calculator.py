import streamlit as st

st.set_page_config(page_title="Partner Activation Incentive", page_icon="🧮", layout="centered")

SLABS = [
    ("S1", "25K–50K"),
    ("S2", "50K–1L"),
    ("S3", "1L–2L"),
    ("S4", "2L–5L"),
    ("S5", ">5L"),
]

RATES = {
    "S1": {5: 100, 10: 110, 15: 120, 20: 130, 25: 150},
    "S2": {5: 110, 10: 120, 15: 130, 20: 150, 25: 175},
    "S3": {5: 120, 10: 130, 15: 150, 20: 175, 25: 200},
    "S4": {5: 130, 10: 150, 15: 175, 20: 200, 25: 225},
    "S5": {5: 150, 10: 175, 15: 200, 20: 225, 25: 250},
}

# Backend-only — never shown in the UI.
REACTIVATION_MULTIPLIER = 1.25


def tier_for_total(total: int) -> int:
    """One shared tier for all 5 slabs, from the total activation count:
    floor to the nearest completed multiple of 5, capped at 25.
    e.g. 20 -> 20, 19 -> 15, 25 -> 25, 30 -> 25.
    """
    floored = (total // 5) * 5
    return min(25, max(5, floored))


# Aggressively trim Streamlit's default chrome and spacing so this fits one screen.
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        max-width: 460px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlock"] { gap: 0.3rem !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0.4rem !important; margin-bottom: -0.7rem; }
    div[data-testid="stNumberInput"] input { padding: 0.2rem 0.4rem; font-size: 0.82rem; }
    div[data-testid="stNumberInput"] { margin-bottom: 0 !important; }
    h3 { margin-bottom: 0.3rem !important; padding-top: 0 !important; }
    hr { margin: 0.4rem 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Partner Activation Incentive")

total_activation = st.number_input("Total count of activation", min_value=0, step=1, value=0)
tier = tier_for_total(int(total_activation))  # not shown anywhere in the UI

h1, h2, h3, h4 = st.columns([1.3, 0.9, 0.9, 1.1])
h1.markdown("<span style='font-size:11px;color:gray'>Slab</span>", unsafe_allow_html=True)
h2.markdown("<span style='font-size:11px;color:gray'>Active</span>", unsafe_allow_html=True)
h3.markdown("<span style='font-size:11px;color:gray'>Inactive</span>", unsafe_allow_html=True)
h4.markdown("<span style='font-size:11px;color:gray'>Incentive</span>", unsafe_allow_html=True)

slab_sum = 0
total_incentive = 0.0

for slab_id, label in SLABS:
    c1, c2, c3, c4 = st.columns([1.3, 0.9, 0.9, 1.1])
    c1.markdown(
        f"<span style='font-weight:600;font-size:13px'>{slab_id}</span> "
        f"<span style='color:gray;font-size:10.5px'>{label}</span>",
        unsafe_allow_html=True,
    )
    active = c2.number_input(
        f"Active {slab_id}", min_value=0, step=1, value=0,
        key=f"active_{slab_id}", label_visibility="collapsed",
    )
    inactive = c3.number_input(
        f"Inactive {slab_id}", min_value=0, step=1, value=0,
        key=f"inactive_{slab_id}", label_visibility="collapsed",
    )

    rate = RATES[slab_id][tier]
    incentive = rate * active + rate * inactive * REACTIVATION_MULTIPLIER
    c4.markdown(
        f"<div style='text-align:right; padding-top:6px; font-size:13px'>{incentive:,.0f}</div>",
        unsafe_allow_html=True,
    )

    slab_sum += active + inactive
    total_incentive += incentive

st.markdown("<hr>", unsafe_allow_html=True)

col_a, col_b = st.columns([1, 1])
with col_a:
    if total_activation != 0 or slab_sum != 0:
        if total_activation == slab_sum:
            st.markdown("<span style='color:#1F5C56;font-size:12px'>Matches ✓</span>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<span style='color:#9C4A34;font-size:12px'>Slabs total {slab_sum}</span>",
                unsafe_allow_html=True,
            )
    st.button("Reset", key="reset_btn")

with col_b:
    st.markdown(
        f"""
        <div style='text-align:right'>
            <span style='color:gray;font-size:11px'>Total incentive</span><br>
            <span style='font-size:24px;font-weight:700;color:#B4842A'>₹{total_incentive:,.0f}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.session_state.get("reset_btn"):
    for slab_id, _ in SLABS:
        st.session_state[f"active_{slab_id}"] = 0
        st.session_state[f"inactive_{slab_id}"] = 0
    st.rerun()
