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

    agg_user = pd.read_sql_query(
        "SELECT * FROM Aggregated_user",
        conn
    )

    agg_txn = pd.read_sql_query(
        "SELECT * FROM Aggregated_transaction",
        conn
    )

    conn.close()

    agg_user = preprocess_data(agg_user)
    agg_txn = preprocess_data(agg_txn)

    return agg_user, agg_txn


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

def render_kpis(agg_user, agg_txn):

    india_users = agg_user[
        agg_user['State'] == 'India'
    ]

    india_txn = agg_txn[
        agg_txn['State'] == 'India'
    ]

    total_txn_amount = int(
        india_txn['Transaction_amount'].sum()
    )

    total_txn_count = int(
        india_txn['Transaction_count'].sum()
    )

    total_brands = int(
        india_users['User_brand'].nunique()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Transaction Amount",
        f"₹ {total_txn_amount:,.0f}"
    )

    col2.metric(
        "Total Transactions",
        f"{total_txn_count:,}"
    )

    col3.metric(
        "Smartphone Brands",
        total_brands
    )


# =========================================================
# TRANSACTION TYPE ANALYSIS
# =========================================================

def render_transaction_type_analysis(agg_txn):

    st.subheader("Transaction Type Analysis")

    india_txn = agg_txn[
        agg_txn['State'] == 'India'
    ]

    txn_type = (
        india_txn.groupby('Transaction_type')[
            'Transaction_amount'
        ]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        txn_type,
        x='Transaction_amount',
        y='Transaction_type',
        orientation='h',
        color='Transaction_amount',
        color_continuous_scale='viridis',
        text_auto='.2s'
    )

    fig.update_layout(
        height=500,
        showlegend=False,
        xaxis_title='Transaction Amount',
        yaxis_title='Transaction Type'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# ATV ANALYSIS BY TRANSACTION TYPE
# =========================================================

def render_atv_by_transaction_type(agg_txn):

    st.subheader("ATV by Transaction Type")

    india_txn = agg_txn[
        agg_txn['State'] == 'India'
    ]

    atv_data = (
        india_txn.groupby('Transaction_type')[
            ['Transaction_amount', 'Transaction_count']
        ]
        .sum()
        .reset_index()
    )

    atv_data['ATV'] = (
        atv_data['Transaction_amount']
        /
        atv_data['Transaction_count']
    )

    atv_data = atv_data.sort_values(
        by='ATV',
        ascending=False
    )

    fig = px.bar(
        atv_data,
        x='Transaction_type',
        y='ATV',
        color='ATV',
        color_continuous_scale='magma',
        text_auto='.2s'
    )

    fig.update_layout(
        height=450,
        xaxis_title='Transaction Type',
        yaxis_title='Average Transaction Value'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# ATV ANALYSIS BY STATE
# =========================================================

def render_atv_by_state(agg_txn, top_n=15):

    st.subheader("Top States by ATV")

    state_txn = agg_txn[
        agg_txn['State'] != 'India'
    ]

    atv_state = (
        state_txn.groupby('State')[
            ['Transaction_amount', 'Transaction_count']
        ]
        .sum()
        .reset_index()
    )

    atv_state['ATV'] = (
        atv_state['Transaction_amount']
        /
        atv_state['Transaction_count']
    )

    atv_state = (
        atv_state.sort_values(
            by='ATV',
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(
        atv_state,
        x='ATV',
        y='State',
        orientation='h',
        color='ATV',
        color_continuous_scale='RdBu',
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
# SMARTPHONE ECOSYSTEM ANALYSIS
# =========================================================

# =========================================================
# BUDGET VS PREMIUM SMARTPHONE ADOPTION
# =========================================================

def render_smartphone_ecosystem(agg_user):

    st.subheader(
        "Budget vs Premium Smartphone Adoption"
    )

    st.markdown(
        """
        Compare PhonePe adoption across
        budget and premium smartphone
        ecosystems.
        """
    )

    # =====================================================
    # BRAND SEGMENTS
    # =====================================================

    budget_brands = [
        'Xiaomi',
        'Vivo',
        'Oppo',
        'Realme',
        'Motorola',
        'Lenovo'
    ]

    premium_brands = [
        'Samsung',
        'Apple',
        'OnePlus'
    ]

    brand_category = {
        **{
            brand: 'Budget'
            for brand in budget_brands
        },

        **{
            brand: 'Premium'
            for brand in premium_brands
        }
    }

    # =====================================================
    # INDIA DATA
    # =====================================================

    india_df = agg_user[
        agg_user['State'] == 'India'
    ].copy()

    india_df['Segment'] = (
        india_df['User_brand']
        .map(brand_category)
    )

    india_df = india_df.dropna(
        subset=['Segment']
    )

    # =====================================================
    # AGGREGATION
    # =====================================================

    segment_brand_df = (
        india_df.groupby(
            ['Segment', 'User_brand']
        )['User_count']
        .sum()
        .reset_index()
    )

    # =====================================================
    # STACKED BAR CHART
    # =====================================================

    fig = px.bar(
        segment_brand_df,
        x='Segment',
        y='User_count',
        color='User_brand',
        text_auto='.2s',
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig.update_layout(
        height=600,
        xaxis_title='Smartphone Segment',
        yaxis_title='PhonePe Users',
        legend_title='Brands',
        hovermode='x unified'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# USER ENGAGEMENT TREND
# =========================================================

def render_user_engagement_trend(agg_user):

    st.subheader("Quarter-wise User Engagement Trend")

    india_users = agg_user[
        agg_user['State'] == 'India'
    ]

    engagement = (
        india_users.groupby(
            ['Year', 'Quarter']
        )['App_opens']
        .max()
        .reset_index()
    )

    fig = px.line(
        engagement,
        x='Year',
        y='App_opens',
        color='Quarter',
        markers=True
    )

    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis_title='Year',
        yaxis_title='App Opens'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MAIN SECTION FUNCTION
# =========================================================

def show_section2(selected_years, selected_quarters):

    st.header("SECTION 2 — User & Payment Behavior")

    st.markdown(
        """
        Analyze transaction behavior, smartphone ecosystem,
        payment patterns, and user engagement trends.
        """
    )

    agg_user, agg_txn = load_data()

    agg_user = apply_filters(
        agg_user,
        selected_years,
        selected_quarters
    )

    agg_txn = apply_filters(
        agg_txn,
        selected_years,
        selected_quarters
    )

    # KPI ROW
    render_kpis(agg_user, agg_txn)

    st.markdown("---")

    # PRIMARY ANALYSIS
    render_transaction_type_analysis(agg_txn)

    st.markdown("---")

    # COMPARATIVE ANALYSIS
    col1, col2 = st.columns(2)

    with col1:
        render_atv_by_transaction_type(agg_txn)

    with col2:
        render_atv_by_state(agg_txn)

    st.markdown("---")

    # SMARTPHONE ANALYSIS
    render_smartphone_ecosystem(agg_user)

    st.markdown("---")

    # USER ENGAGEMENT
    render_user_engagement_trend(agg_user)