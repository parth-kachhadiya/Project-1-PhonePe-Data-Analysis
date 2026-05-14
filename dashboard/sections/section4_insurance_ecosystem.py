import sqlite3

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.preprocessing import preprocess_data


# =========================================================
# LOAD DATA
# =========================================================

DB_PATH = "..\\database\\phonepe_data.db"

@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    agg_insurance = pd.read_sql_query(
        "SELECT * FROM aggregated_insurance",
        conn
    )

    map_insurance = pd.read_sql_query(
        "SELECT * FROM map_insurance",
        conn
    )

    conn.close()

    agg_insurance = preprocess_data(
        agg_insurance
    )

    map_insurance = preprocess_data(
        map_insurance
    )

    return agg_insurance, map_insurance


# =========================================================
# FILTER DATA
# =========================================================

def apply_filters(df, years, quarters):

    df = df[
        df['Year'].isin(years)
    ]

    df = df[
        df['Quarter'].isin(quarters)
    ]

    return df


# =========================================================
# KPI SECTION
# =========================================================

def render_kpis(agg_insurance, map_insurance):

    india_data = agg_insurance[
        agg_insurance['State'] == 'India'
    ]

    regional_data = map_insurance[
        map_insurance['State'] != 'India'
    ]

    total_txn = int(
        india_data['Transaction_count'].sum()
    )

    total_amount = int(
        india_data['Transaction_amount'].sum()
    )

    total_districts = int(
        regional_data['District'].nunique()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Insurance Transactions",
        f"{total_txn:,}"
    )

    col2.metric(
        "Insurance Amount",
        f"₹ {total_amount:,.0f}"
    )

    col3.metric(
        "Insurance Active Districts",
        total_districts
    )


# =========================================================
# INSURANCE TRANSACTION GROWTH
# =========================================================

def render_insurance_transaction_growth(
    agg_insurance
):

    st.subheader(
        "Insurance Transaction Growth"
    )

    india_data = agg_insurance[
        agg_insurance['State'] == 'India'
    ]

    trend = (
        india_data.groupby(
            ['Year', 'Quarter']
        )['Transaction_count']
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x='Year',
        y='Transaction_count',
        color='Quarter',
        markers=True
    )

    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis_title='Year',
        yaxis_title='Transaction Count'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# INSURANCE AMOUNT GROWTH
# =========================================================

def render_insurance_amount_growth(
    agg_insurance
):

    st.subheader(
        "Insurance Transaction Amount Growth"
    )

    india_data = agg_insurance[
        agg_insurance['State'] == 'India'
    ]

    trend = (
        india_data.groupby(
            ['Year', 'Quarter']
        )['Transaction_amount']
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x='Year',
        y='Transaction_amount',
        color='Quarter',
        markers=True
    )

    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis_title='Year',
        yaxis_title='Transaction Amount'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# INTERACTIVE INSURANCE STATE EXPLORER
# =========================================================

def render_insurance_state_explorer(
    agg_insurance
):

    st.subheader(
        "Interactive Insurance State Explorer"
    )

    st.markdown(
        """
        Dynamically explore insurance
        transaction trends for a selected
        state and year.
        """
    )

    # =====================================================
    # REMOVE INDIA
    # =====================================================

    explorer_data = agg_insurance[
        agg_insurance['State'] != 'India'
    ]

    # =====================================================
    # LOCAL FILTERS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_state = st.selectbox(
            "Select State",
            sorted(
                explorer_data['State']
                .unique()
            ),
            key='insurance_state'
        )

    with col2:

        selected_year = st.selectbox(
            "Select Year",
            sorted(
                explorer_data['Year']
                .unique()
            ),
            key='insurance_year'
        )

    with col3:

        metric = st.selectbox(
            "Select Metric",
            [
                'Transaction_count',
                'Transaction_amount'
            ],
            key='insurance_metric'
        )

    # =====================================================
    # FILTER DATA
    # =====================================================

    state_df = explorer_data[
        (
            explorer_data['State']
            == selected_state
        )
        &
        (
            explorer_data['Year']
            == selected_year
        )
    ]

    # =====================================================
    # QUARTERLY ANALYSIS
    # =====================================================

    quarter_df = (
        state_df.groupby('Quarter')[
            metric
        ]
        .sum()
        .reset_index()
    )

    # =====================================================
    # DYNAMIC TITLE
    # =====================================================

    metric_title = (
        "Transaction Count"
        if metric == 'Transaction_count'
        else "Transaction Amount"
    )

    # =====================================================
    # PLOT
    # =====================================================

    fig = px.bar(
        quarter_df,
        x='Quarter',
        y=metric,
        color=metric,
        color_continuous_scale='Turbo',
        text_auto='.2s'
    )

    fig.update_layout(
        height=550,
        showlegend=False,
        xaxis_title='Quarter',
        yaxis_title=metric_title,
        title=f'{selected_state} - {metric_title} Analysis ({selected_year})'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# INSURANCE ATV ANALYSIS
# =========================================================

def render_insurance_atv_analysis(
    map_insurance,
    top_n=15
):

    st.subheader(
        "Insurance ATV Analysis"
    )

    state_data = map_insurance[
        map_insurance['State'] != 'India'
    ]

    atv = (
        state_data.groupby('State')[
            [
                'Transaction_amount',
                'Transaction_count'
            ]
        ]
        .sum()
        .reset_index()
    )

    atv['ATV'] = (
        atv['Transaction_amount']
        /
        atv['Transaction_count']
    )

    atv = (
        atv.sort_values(
            by='ATV',
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(
        atv,
        x='ATV',
        y='State',
        orientation='h',
        color='ATV',
        color_continuous_scale='sunset',
        text_auto='.2s'
    )

    fig.update_layout(
        height=550,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# STATE INSURANCE PENETRATION
# =========================================================

def render_state_insurance_penetration(
    map_insurance,
    top_n=15
):

    st.subheader(
        "Top Insurance Adoption States"
    )

    state_data = map_insurance[
        map_insurance['State'] != 'India'
    ]

    penetration = (
        state_data.groupby('State')[
            'Transaction_count'
        ]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        penetration,
        x='Transaction_count',
        y='State',
        orientation='h',
        color='Transaction_count',
        color_continuous_scale='viridis',
        text_auto='.2s'
    )

    fig.update_layout(
        height=550,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DISTRICT INSURANCE PENETRATION
# =========================================================

def render_district_insurance_penetration(
    map_insurance,
    top_n=15
):

    st.subheader(
        "Top Insurance Adoption Districts"
    )

    district_data = map_insurance[
        map_insurance['State'] != 'India'
    ]

    penetration = (
        district_data.groupby('District')[
            'Transaction_count'
        ]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        penetration,
        x='Transaction_count',
        y='District',
        orientation='h',
        color='Transaction_count',
        color_continuous_scale='magma',
        text_auto='.2s'
    )

    fig.update_layout(
        height=550,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# HOT QUARTER ANALYSIS
# =========================================================

def render_hot_quarter_insurance(
    agg_insurance
):

    st.subheader(
        "Hot Quarter of Buying Insurance"
    )

    india_data = agg_insurance[
        agg_insurance['State'] == 'India'
    ]

    quarter_data = (
        india_data.groupby(
            ['Year', 'Quarter']
        )['Transaction_count']
        .sum()
        .reset_index()
    )

    fig = px.bar(
        quarter_data,
        x='Year',
        y='Transaction_count',
        color='Quarter',
        barmode='group',
        text_auto='.2s'
    )

    fig.update_layout(
        height=500,
        xaxis_title='Year',
        yaxis_title='Transaction Count'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MAIN SECTION FUNCTION
# =========================================================

def show_section4(
    selected_years,
    selected_quarters
):

    st.header(
        "SECTION 4 — Insurance Ecosystem"
    )

    st.markdown(
        """
        Analyze insurance growth, adoption,
        transaction behavior, and regional
        insurance penetration across India.
        """
    )

    agg_insurance, map_insurance = load_data()

    agg_insurance = apply_filters(
        agg_insurance,
        selected_years,
        selected_quarters
    )

    map_insurance = apply_filters(
        map_insurance,
        selected_years,
        selected_quarters
    )

    # KPI ROW
    render_kpis(
        agg_insurance,
        map_insurance
    )

    st.markdown("---")

    # PRIMARY GROWTH ANALYSIS
    render_insurance_transaction_growth(
        agg_insurance
    )

    render_insurance_amount_growth(
        agg_insurance
    )
    st.markdown("---")

    # INTERACTIVE INSURANCE EXPLORER
    render_insurance_state_explorer(
        agg_insurance
    )

    st.markdown("---")

    st.markdown("---")

    # ATV + HOT QUARTER
    col1, col2 = st.columns(2)

    with col1:
        render_insurance_atv_analysis(
            map_insurance
        )

    with col2:
        render_hot_quarter_insurance(
            agg_insurance
        )

    st.markdown("---")

    # REGIONAL PENETRATION
    col1, col2 = st.columns(2)

    with col1:
        render_state_insurance_penetration(
            map_insurance
        )

    with col2:
        render_district_insurance_penetration(
            map_insurance
        )