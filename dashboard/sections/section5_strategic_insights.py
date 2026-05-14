import sqlite3

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.preprocessing import (
    preprocess_data,
    handle_missing_app_opens
)


# =========================================================
# LOAD DATA
# =========================================================

DB_PATH = "..\\database\\phonepe_data.db"

@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    map_user = pd.read_sql_query(
        "SELECT * FROM map_user",
        conn
    )

    map_map = pd.read_sql_query(
        "SELECT * FROM map_map",
        conn
    )

    conn.close()

    map_user = preprocess_data(
        map_user
    )

    map_map = preprocess_data(
        map_map
    )

    map_user = handle_missing_app_opens(
        map_user
    )

    return map_user, map_map


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

def render_kpis(map_user, map_map):

    regional_users = map_user[
        map_user['State'] != 'India'
    ]

    regional_txn = map_map[
        map_map['State'] != 'India'
    ]

    total_users = int(
        regional_users['Registered_users']
        .sum()
    )

    total_transactions = int(
        regional_txn['Transaction_count']
        .sum()
    )

    total_amount = int(
        regional_txn['Transaction_amount']
        .sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Regional Users",
        f"{total_users:,}"
    )

    col2.metric(
        "Regional Transactions",
        f"{total_transactions:,}"
    )

    col3.metric(
        "Transaction Amount",
        f"₹ {total_amount:,.0f}"
    )


# =========================================================
# POTENTIAL USER SEGMENTS
# =========================================================

def render_potential_user_segments(
    map_user,
    top_n=15
):

    st.subheader(
        "Potential User Segments"
    )

    district_data = map_user[
        map_user['State'] != 'India'
    ]

    engagement = (
        district_data.groupby('District')[
            [
                'Registered_users',
                'App_opens'
            ]
        ]
        .sum()
        .reset_index()
    )

    engagement = engagement.dropna(
        subset=['App_opens']
    )

    engagement['App_Opens_Per_User'] = (
        engagement['App_opens']
        /
        engagement['Registered_users']
    )

    engagement = (
        engagement.sort_values(
            by=[
                'Registered_users',
                'App_Opens_Per_User'
            ],
            ascending=[False, True]
        )
        .head(top_n)
    )

    fig = px.bar(
        engagement,
        x='Registered_users',
        y='District',
        orientation='h',
        color='App_Opens_Per_User',
        color_continuous_scale='sunset',
        text_auto='.2s'
    )

    fig.update_layout(
        height=650,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# POTENTIAL GROWTH REGIONS
# =========================================================

def render_potential_growth_regions(
    map_user,
    top_n=15
):

    st.subheader(
        "Potential Growth Regions"
    )

    district_data = map_user[
        map_user['State'] != 'India'
    ]

    yearly_users = (
        district_data.groupby(
            ['District', 'Year']
        )['Registered_users']
        .sum()
        .reset_index()
    )

    growth = (
        yearly_users.groupby('District')
        .agg(
            First_Year=(
                'Registered_users',
                'first'
            ),
            Last_Year=(
                'Registered_users',
                'last'
            )
        )
        .reset_index()
    )

    growth = growth[
        growth['First_Year'] > 0
    ]

    growth['Growth_%'] = (
        (
            growth['Last_Year']
            -
            growth['First_Year']
        )
        /
        growth['First_Year']
    ) * 100

    growth = (
        growth.sort_values(
            by='Growth_%',
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(
        growth,
        x='Growth_%',
        y='District',
        orientation='h',
        color='Growth_%',
        color_continuous_scale='Tealgrn',
        text_auto='.2f'
    )

    fig.update_layout(
        height=650,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# UNUSUAL TRANSACTION PATTERNS
# =========================================================

def render_unusual_transaction_patterns(
    map_map
):

    st.subheader(
        "Unusual Transaction Pattern Detection"
    )

    state_data = map_map[
        map_map['State'] != 'India'
    ]

    txn = (
        state_data.groupby(
            ['State', 'Year']
        )['Transaction_amount']
        .sum()
        .reset_index()
    )

    top_states = (
        txn.groupby('State')[
            'Transaction_amount'
        ]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .index
    )

    txn = txn[
        txn['State'].isin(top_states)
    ]

    fig = px.box(
        txn,
        x='State',
        y='Transaction_amount',
        points='outliers'
    )

    fig.update_layout(
        height=650,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# HIGH VALUE VS HIGH FREQUENCY
# =========================================================

def render_high_value_vs_frequency(
    map_map
):

    st.subheader(
        "High-Value vs High-Frequency Regions"
    )

    district_data = map_map[
        map_map['State'] != 'India'
    ]

    region_data = (
        district_data.groupby('District')[
            [
                'Transaction_amount',
                'Transaction_count'
            ]
        ]
        .sum()
        .reset_index()
    )

    # TOP 15 by transaction amount — outlier focus
    region_data = (
        region_data.sort_values(
            by='Transaction_amount',
            ascending=False
        )
        .head(15)
        .reset_index(drop=True)
    )

    import plotly.graph_objects as go

    # ATV calculated inline — avoids NaN column issues
    atv_vals = [
        round(amt / cnt, 2)
        if cnt and cnt > 0
        else 0
        for amt, cnt in zip(
            region_data['Transaction_amount'],
            region_data['Transaction_count']
        )
    ]

    fig = go.Figure(
        go.Treemap(
            labels=region_data['District'].tolist(),
            parents=[''] * len(region_data),
            values=region_data['Transaction_amount'].tolist(),
            marker=dict(
                colors=atv_vals,
                colorscale='RdYlGn',
                colorbar=dict(title='ATV (₹)'),
                showscale=True
            ),
            customdata=list(
                zip(
                    region_data['Transaction_count'].tolist(),
                    atv_vals,
                    region_data['Transaction_amount'].tolist()
                )
            ),
            texttemplate=(
                "<b>%{label}</b><br>"
                "Amount: ₹%{value:,.0f}<br>"
                "ATV: ₹%{customdata[1]:,.0f}"
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Total Amount: ₹%{customdata[2]:,.0f}<br>"
                "Txn Count: %{customdata[0]:,}<br>"
                "ATV: ₹%{customdata[1]:,.0f}<br>"
                "<extra></extra>"
            ),
            textfont=dict(size=13)
        )
    )

    fig.update_layout(
        height=700,
        title='Top 15 Districts — Box size = Total Amount | Color = ATV'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MAIN SECTION FUNCTION
# =========================================================

def show_section5(
    selected_years,
    selected_quarters
):

    st.header(
        "SECTION 5 — Strategic Insights"
    )

    st.markdown(
        """
        Identify hidden opportunities,
        unusual transaction behavior,
        engagement gaps, and future
        growth regions across India.
        """
    )

    map_user, map_map = load_data()

    map_user = apply_filters(
        map_user,
        selected_years,
        selected_quarters
    )

    map_map = apply_filters(
        map_map,
        selected_years,
        selected_quarters
    )

    # KPI ROW
    render_kpis(
        map_user,
        map_map
    )

    st.markdown("---")

    # LARGE INSIGHT GRAPH
    render_potential_user_segments(
        map_user
    )

    st.markdown("---")

    # LARGE INSIGHT GRAPH
    render_potential_growth_regions(
        map_user
    )

    st.markdown("---")

    # LARGE HORIZONTAL GRAPH
    render_unusual_transaction_patterns(
        map_map
    )

    st.markdown("---")

    # FULL WIDTH STRATEGIC GRAPH
    render_high_value_vs_frequency(
        map_map
    )