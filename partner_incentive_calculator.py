import streamlit as st

st.set_page_config(page_title="Partner Activation Incentive", page_icon="🧮", layout="centered")

# Slab table, as supplied: row = SIP amount slab, column = partner-count tier (5/10/15/20/25).
SLABS = [
    ("S1", "₹25K–50K"),
    ("S2", "₹50K–1L"),
    ("S3", "₹1L–2L"),
    ("S4", "₹2L–5L"),
    ("S5", ">₹5L"),
]

TIERS = [5, 10, 15, 20, 25]

RATES = {
    "S1": {5: 100, 10: 110, 15: 120, 20: 130, 25: 150},
    "S2": {5: 110, 10: 120, 15: 130, 20: 150, 25: 175},
    "S3": {5: 120, 10: 130, 15: 150, 20: 175, 25: 200},
    "S4": {5: 130, 10: 150, 15: 175, 20: 200, 25: 225},
    "S5": {5: 150, 10: 175, 15: 200, 20: 225, 25: 250},
}

# Backend-only — never shown in the UI.
REACTIVATION_MULTIPLIER = 1.25

st.markdown(
    """
    <style>
    .block-container { padding-top: 2.2rem; padding-bottom: 1.5rem; max-width: 660px; }
    div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] { margin-bottom: -0.6rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Partner Activation Incentive")
st.caption("Pick each slab's partner-count tier, then split it into active and inactive.")

total_partner_count = st.number_input("Total partner count", min_value=0, step=1, value=0)

st.write("")
h1, h2, h3, h4, h5 = st.columns([1.3, 0.9, 0.9, 0.9, 1.1])
h1.markdown("**Slab**")
h2.markdown("**Tier**")
h3.markdown("**Active**")
h4.markdown("**Inactive**")
h5.markdown("**Incentive**")

tier_sum = 0
total_incentive = 0.0

for slab_id, label in SLABS:
    c1, c2, c3, c4, c5 = st.columns([1.3, 0.9, 0.9, 0.9, 1.1])
    c1.markdown(
        f"**{slab_id}**  \n<span style='color:gray;font-size:12px'>{label}</span>",
        unsafe_allow_html=True,
    )
    tier = c2.selectbox(
        f"Tier {slab_id}", TIERS, index=0,
        key=f"tier_{slab_id}", label_visibility="collapsed",
    )
    active = c3.number_input(
        f"Active {slab_id}", min_value=0, step=1, value=0,
        key=f"active_{slab_id}", label_visibility="collapsed",
    )
    inactive = c4.number_input(
        f"Inactive {slab_id}", min_value=0, step=1, value=0,
        key=f"inactive_{slab_id}", label_visibility="collapsed",
    )

    rate = RATES[slab_id][tier]
    incentive = rate * (active + REACTIVATION_MULTIPLIER * inactive)
    c5.markdown(
        f"<div style='text-align:right; padding-top:8px'>{incentive:,.0f}</div>",
        unsafe_allow_html=True,
    )

    tier_sum += tier
    total_incentive += incentive

st.write("---")

col_a, col_b = st.columns([1, 1])
with col_a:
    if total_partner_count == 0:
        pass
    elif total_partner_count == tier_sum:
        st.success("Matches tiers", icon="✅")
    else:
        st.error(f"Tiers add up to {tier_sum}, not {total_partner_count}")

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
