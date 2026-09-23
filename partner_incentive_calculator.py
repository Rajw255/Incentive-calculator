import streamlit as st

st.set_page_config(page_title="Partner Activation Incentive", page_icon="🧮", layout="centered")

SLABS = [
    ("S1", "₹25K–50K"),
    ("S2", "₹50K–1L"),
    ("S3", "₹1L–2L"),
    ("S4", "₹2L–5L"),
    ("S5", ">₹5L"),
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


st.markdown(
    """
    <style>
    .block-container { padding-top: 2.2rem; padding-bottom: 1.5rem; max-width: 620px; }
    div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] { margin-bottom: -0.6rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Partner Activation Incentive")
st.caption("Enter your total activation count, then active and inactive partners per slab.")

total_activation = st.number_input("Total count of activation", min_value=0, step=1, value=0)
tier = tier_for_total(int(total_activation))  # not shown anywhere in the UI

st.write("")
h1, h2, h3, h4 = st.columns([1.4, 1, 1, 1.3])
h1.markdown("**Slab**")
h2.markdown("**Active**")
h3.markdown("**Inactive**")
h4.markdown("**Incentive**")

slab_sum = 0
total_incentive = 0.0

for slab_id, label in SLABS:
    c1, c2, c3, c4 = st.columns([1.4, 1, 1, 1.3])
    c1.markdown(
        f"**{slab_id}**  \n<span style='color:gray;font-size:12px'>{label}</span>",
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
        f"<div style='text-align:right; padding-top:8px'>{incentive:,.0f}</div>",
        unsafe_allow_html=True,
    )

    slab_sum += active + inactive
    total_incentive += incentive

st.write("---")

col_a, col_b = st.columns([1, 1])
with col_a:
    if total_activation == 0 and slab_sum == 0:
        pass
    elif total_activation == slab_sum:
        st.success("Matches", icon="✅")
    else:
        st.error(f"Slabs total {slab_sum}, not {int(total_activation)}")

with col_b:
    st.markdown(
        f"""
        <div style='text-align:right'>
            <span style='color:gray;font-size:13px'>Total incentive</span><br>
            <span style='font-size:32px;font-weight:700;color:#B4842A'>₹{total_incentive:,.0f}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
