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

    conn.close()

    map_user = preprocess_data(map_user)

    map_user = handle_missing_app_opens(map_user)

    return map_user


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

def render_kpis(map_user):

    regional_data = map_user[
        map_user['State'] != 'India'
    ]

    total_users = int(
        regional_data['Registered_users'].sum()
    )

    total_app_opens = int(
        regional_data['App_opens'].sum(skipna=True)
    )

    total_districts = int(
        regional_data['District'].nunique()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Regional Users",
        f"{total_users:,}"
    )

    col2.metric(
        "App Opens",
        f"{total_app_opens:,}"
    )

    col3.metric(
        "Active Districts",
        total_districts
    )


# =========================================================
# TOP STATES
# =========================================================

def render_top_states(map_user, top_n=15):

    st.subheader("Top Performing States")

    state_data = map_user[
        map_user['State'] != 'India'
    ]

    top_states = (
        state_data.groupby('State')[
            'Registered_users'
        ]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        top_states,
        x='Registered_users',
        y='State',
        orientation='h',
        color='Registered_users',
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
# TOP DISTRICTS
# =========================================================

def render_top_districts(map_user, top_n=15):

    st.subheader("Top Performing Districts")

    district_data = map_user[
        map_user['State'] != 'India'
    ]

    top_districts = (
        district_data.groupby('District')[
            'Registered_users'
        ]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        top_districts,
        x='Registered_users',
        y='District',
        orientation='h',
        color='Registered_users',
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
# STATE DISTRICT EXPLORER
# =========================================================

def render_state_district_explorer(map_user):

    st.subheader(
        "Interactive State District Explorer"
    )

    st.markdown(
        """
        Dynamically explore district-level
        adoption and engagement trends
        for a selected state.
        """
    )

    # =====================================================
    # LOCAL FILTERS
    # =====================================================

    explorer_data = map_user[
        map_user['State'] != 'India'
    ]

    states = sorted(
        explorer_data['State'].unique()
    )

    col1, col2 = st.columns([2, 1])

    with col1:

        selected_state = st.selectbox(
            "Select State",
            states,
            key='district_explorer_state'
        )

    with col2:

        top_k = st.slider(
            "Top Districts",
            min_value=5,
            max_value=25,
            value=10,
            step=1,
            key='district_explorer_topk'
        )

    # =====================================================
    # FILTER STATE
    # =====================================================

    state_df = explorer_data[
        explorer_data['State']
        == selected_state
    ]

    # =====================================================
    # DISTRICT AGGREGATION
    # =====================================================

    district_summary = (
        state_df.groupby('District')[
            [
                'Registered_users',
                'App_opens'
            ]
        ]
        .sum()
        .reset_index()
    )

    district_summary = district_summary.dropna(
        subset=['App_opens']
    )

    district_summary['Engagement_ratio'] = (
        district_summary['App_opens']
        /
        district_summary['Registered_users']
    )

    district_summary = (
        district_summary.sort_values(
            by='Registered_users',
            ascending=False
        )
        .head(top_k)
    )

    # =====================================================
    # FULL WIDTH GRAPH
    # =====================================================

    fig = px.bar(
        district_summary,
        x='Registered_users',
        y='District',
        orientation='h',
        color='Engagement_ratio',
        color_continuous_scale='Turbo',
        text_auto='.2s',
        hover_data=[
            'App_opens',
            'Engagement_ratio'
        ]
    )

    fig.update_layout(
        height=650,
        showlegend=False,
        xaxis_title='Registered Users',
        yaxis_title='District',
        coloraxis_colorbar_title='Engagement'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# EMERGING GROWTH DISTRICTS
# =========================================================

def render_emerging_growth_districts(map_user, top_n=10):

    st.subheader("Emerging Growth Districts")

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
            First_Year=('Registered_users', 'first'),
            Last_Year=('Registered_users', 'last')
        )
        .reset_index()
    )

    growth['Growth_%'] = (
        (
            growth['Last_Year']
            -
            growth['First_Year']
        )
        /
        growth['First_Year']
    ) * 100

    top_growth = (
        growth.sort_values(
            by='Growth_%',
            ascending=False
        )
        .head(top_n)
    )

    trend_data = yearly_users[
        yearly_users['District'].isin(
            top_growth['District']
        )
    ]

    fig = px.line(
        trend_data,
        x='Year',
        y='Registered_users',
        color='District',
        markers=True
    )

    fig.update_layout(
        height=550,
        hovermode='x unified'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# ENGAGEMENT RATIO ANALYSIS
# =========================================================

def render_engagement_ratio_analysis(map_user, top_n=15):

    st.subheader("Top Districts by Engagement Ratio")

    district_data = map_user[
        map_user['State'] != 'India'
    ]

    engagement = (
        district_data.groupby('District')[
            ['Registered_users', 'App_opens']
        ]
        .sum()
        .reset_index()
    )

    engagement = engagement.dropna(
        subset=['App_opens']
    )

    engagement['Engagement_ratio'] = (
        engagement['App_opens']
        /
        engagement['Registered_users']
    )

    ratio = (
        engagement.sort_values(
            by='Engagement_ratio',
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(
        ratio,
        x='Engagement_ratio',
        y='District',
        orientation='h',
        color='Engagement_ratio',
        color_continuous_scale='RdBu',
        text_auto='.2f'
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
# STATE GROWTH HOTSPOTS
# =========================================================

def render_state_growth_hotspots(map_user):

    st.subheader("State Growth Hotspots")

    state_data = map_user[
        map_user['State'] != 'India'
    ]

    yearly_users = (
        state_data.groupby(
            ['State', 'Year']
        )['Registered_users']
        .sum()
        .reset_index()
    )

    fig = px.density_heatmap(
        yearly_users,
        x='Year',
        y='State',
        z='Registered_users',
        color_continuous_scale='YlGnBu'
    )

    fig.update_layout(
        height=700
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DISTRICT GROWTH HOTSPOTS
# =========================================================

def render_district_growth_hotspots(map_user, top_n=15):

    st.subheader("Regional Growth Hotspots")

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
            First_Year=('Registered_users', 'first'),
            Last_Year=('Registered_users', 'last')
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
        color_continuous_scale='sunset',
        text_auto='.2f'
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
# MAIN SECTION FUNCTION
# =========================================================

def show_section3(selected_years, selected_quarters):

    st.header("SECTION 3 — Regional Adoption")

    st.markdown(
        """
        Analyze regional PhonePe adoption,
        engagement behavior, and emerging
        growth hotspots across India.
        """
    )

    map_user = load_data()

    map_user = apply_filters(
        map_user,
        selected_years,
        selected_quarters
    )

    # KPI ROW
    render_kpis(map_user)

    st.markdown("---")

    # TOP REGIONS
    col1, col2 = st.columns(2)

    with col1:
        render_top_states(map_user)

    with col2:
        render_top_districts(map_user)

    st.markdown("---")

    # INTERACTIVE DISTRICT EXPLORER
    render_state_district_explorer(map_user)

    st.markdown("---")

    st.markdown("---")

    # GROWTH ANALYSIS
    render_emerging_growth_districts(map_user)

    st.markdown("---")

    # ENGAGEMENT ANALYSIS
    render_engagement_ratio_analysis(map_user)

    st.markdown("---")

    # HOTSPOTS

    render_state_growth_hotspots(map_user)

    st.markdown("---")

    render_district_growth_hotspots(map_user)