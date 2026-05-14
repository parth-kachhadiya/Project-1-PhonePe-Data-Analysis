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
# KPI Test
# =========================================================


def render_kpis(agg_user, agg_txn):

    india_users = agg_user[
        agg_user['State'] == 'India'
    ]

    india_txn = agg_txn[
        agg_txn['State'] == 'India'
    ]

    quarterly_users = (
        india_users.groupby(
            ['Year', 'Quarter']
        )['Registered_users']
        .max()
        .reset_index()
    )

    total_users = int(
        quarterly_users['Registered_users'].sum()
    )

    total_transactions = int(
        india_txn['Transaction_count'].sum()
    )

    total_amount = int(
        india_txn['Transaction_amount'].sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Registered Users",
        f"{total_users:,}"
    )

    col2.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )

    col3.metric(
        "Total Transaction Amount",
        f"₹ {total_amount:,.0f}"
    )


# =========================================================
# INDIA USER GROWTH
# =========================================================

def render_india_user_growth(agg_user):

    india_users = agg_user[
        agg_user['State'] == 'India'
    ]

    quarterly_users = (
        india_users.groupby(
            ['Year', 'Quarter']
        )['Registered_users']
        .max()
        .reset_index()
    )

    yearly_users = (
        quarterly_users.groupby('Year')['Registered_users']
        .sum()
        .reset_index()
    )

    fig = px.line(
        yearly_users,
        x='Year',
        y='Registered_users',
        markers=True,
        title='India Registered User Growth Over Years'
    )

    fig.update_layout(
        title_x=0,
        height=500,
        hovermode='x unified'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TRANSACTION GROWTH
# =========================================================

def render_transaction_growth(agg_txn):

    india_txn = agg_txn[
        agg_txn['State'] == 'India'
    ]

    trend = (
        india_txn.groupby(
            ['Year', 'Quarter']
        )[
            ['Transaction_count', 'Transaction_amount']
        ]
        .sum()
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.line(
            trend,
            x='Year',
            y='Transaction_count',
            color='Quarter',
            markers=True,
            title='Transaction Count Growth'
        )

        fig1.update_layout(
            height=450,
            hovermode='x unified'
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        fig2 = px.line(
            trend,
            x='Year',
            y='Transaction_amount',
            color='Quarter',
            markers=True,
            title='Transaction Amount Growth'
        )

        fig2.update_layout(
            height=450,
            hovermode='x unified'
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


# =========================================================
# YOY ANALYSIS
# =========================================================


def render_yoy_analysis(agg_user, agg_txn):

    india_users = agg_user[
        agg_user['State'] == 'India'
    ]

    quarterly_users = (
        india_users.groupby(
            ['Year', 'Quarter']
        )['Registered_users']
        .max()
        .reset_index()
    )

    user_yearly = (
        quarterly_users.groupby('Year')['Registered_users']
        .sum()
        .reset_index()
    )

    user_yearly['User_YoY_Growth_%'] = (
        user_yearly['Registered_users']
        .pct_change() * 100
    )

    india_txn = agg_txn[
        agg_txn['State'] == 'India'
    ]

    txn_yearly = (
        india_txn.groupby('Year')['Transaction_amount']
        .sum()
        .reset_index()
    )

    txn_yearly['Txn_YoY_Growth_%'] = (
        txn_yearly['Transaction_amount']
        .pct_change() * 100
    )

    yoy_df = pd.merge(
        user_yearly[['Year', 'User_YoY_Growth_%']],
        txn_yearly[['Year', 'Txn_YoY_Growth_%']],
        on='Year'
    )

    fig = px.bar(
        yoy_df,
        x='Year',
        y=['User_YoY_Growth_%', 'Txn_YoY_Growth_%'],
        barmode='group',
        title='Year-over-Year Growth Analysis'
    )

    fig.update_layout(
        height=500,
        hovermode='x unified'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# QOQ ANALYSIS
# =========================================================


def render_qoq_growth(agg_user):

    india_users = agg_user[
        agg_user['State'] == 'India'
    ]

    quarterly_users = (
        india_users.groupby(
            ['Year', 'Quarter']
        )['Registered_users']
        .max()
        .reset_index()
    )

    quarterly_users['Year_Quarter'] = (
        quarterly_users['Year'].astype(str)
        + '-Q' +
        quarterly_users['Quarter'].astype(str)
    )

    quarterly_users['QoQ_Growth_%'] = (
        quarterly_users['Registered_users']
        .pct_change() * 100
    )

    fig = px.bar(
        quarterly_users,
        x='Year_Quarter',
        y='QoQ_Growth_%',
        color='QoQ_Growth_%',
        title='Quarter-over-Quarter User Growth'
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MAIN SECTION FUNCTION
# =========================================================


def show_section1(selected_years, selected_quarters):

    st.header("SECTION 1 — PhonePe Platform Growth")

    st.markdown("Analyze PhonePe platform expansion through user and transaction growth trends.")

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

    # KPI SECTION
    render_kpis(agg_user, agg_txn)

    st.markdown("---")

    # PRIMARY INSIGHT
    render_india_user_growth(agg_user)

    st.markdown("---")

    # TRANSACTION ANALYSIS
    render_transaction_growth(agg_txn)

    st.markdown("---")

    # YOY ANALYSIS
    render_yoy_analysis(agg_user, agg_txn)

    st.markdown("---")

    # QOQ ANALYSIS
    render_qoq_growth(agg_user)