import streamlit as st
from sections.section1_platform_growth import show_section1
from sections.section2_user_behaviour import show_section2
from sections.section3_regional_adoption import show_section3
from sections.section4_insurance_ecosystem import show_section4
from sections.section5_strategic_insights import show_section5

st.set_page_config(
    page_title="PhonePe Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Base */
    .stApp { background-color: #0E1117; }

    h1, h2, h3 { color: #FFFFFF; }

    .stMetric {
        background-color: #1A1C23;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #2D2F36;
    }

    /* Sidebar label */
    [data-testid="stSidebar"] .sidebar-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #6B7280;
        margin: 20px 0 8px 0;
    }

    /* Pill overrides — active pill uses PhonePe purple */
    [data-testid="stSidebar"] button[aria-pressed="true"] {
        background-color: #5A189A !important;
        color: #FFFFFF !important;
        border-color: #5A189A !important;
    }
    [data-testid="stSidebar"] button[aria-pressed="false"] {
        background-color: #1A1C23 !important;
        color: #9CA3AF !important;
        border-color: #2D2F36 !important;
    }
    [data-testid="stSidebar"] button:hover {
        border-color: #7B2FBE !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📊 PhonePe Pulse Dashboard")

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-label">Year</p>', unsafe_allow_html=True)
    selected_years = st.pills(
        label="Year",
        options=[2018, 2019, 2020, 2021, 2022, 2023],
        selection_mode="multi",
        default=[2018, 2019, 2020, 2021, 2022, 2023],
        label_visibility="collapsed",
        key="year_pills",
    )

    st.markdown('<p class="sidebar-label">Quarter</p>', unsafe_allow_html=True)
    selected_quarters = st.pills(
        label="Quarter",
        options=[1, 2, 3, 4],
        format_func=lambda q: f"Q{q}",
        selection_mode="multi",
        default=[1, 2, 3, 4],
        label_visibility="collapsed",
        key="quarter_pills",
    )

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Platform Growth",
    "User & Payment",
    "Regional Adoption",
    "Insurance",
    "Strategic Insights",
])

with tab1:
    show_section1(selected_years, selected_quarters)
with tab2:
    show_section2(selected_years, selected_quarters)
with tab3:
    show_section3(selected_years, selected_quarters)
with tab4:
    show_section4(selected_years, selected_quarters)
with tab5:
    show_section5(selected_years, selected_quarters)