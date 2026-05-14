import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def handle_missing_app_opens(map_user):

    """
    Replace invalid App_opens = 0 values
    with NaN for early quarters.

    Affected periods:
    2018-Q1 to 2019-Q1
    """

    condition = (
        (
            map_user['Year'] == 2018
        )
        |
        (
            (map_user['Year'] == 2019)
            &
            (map_user['Quarter'] == 1)
        )
    )

    map_user.loc[
        condition &
        (map_user['App_opens'] == 0),
        'App_opens'
    ] = np.nan

    return map_user


# 1. TOP PERFORMING STATES

def plot_top_states(map_user, top_n=15):

    """
    Identify top states by PhonePe adoption.
    """

    state_data = map_user[
        map_user['State'] != 'India'
    ]

    quarterly_users = (
        state_data.groupby(
            ['State', 'Year', 'Quarter']
        )['Registered_users']
        .max()
        .reset_index()
    )

    top_states = (
        quarterly_users.groupby('State')[
            'Registered_users'
        ]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=top_states,
        y='State',
        x='Registered_users',
        palette='viridis'
    )

    plt.title(
        f'Top {top_n} Performing States',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Registered Users')
    plt.ylabel('State')

    plt.tight_layout()

    plt.show()


# 2. TOP PERFORMING DISTRICTS

def plot_top_districts(map_user, top_n=15):

    """
    Identify top districts by PhonePe adoption.
    """

    district_data = map_user[
        map_user['State'] != 'India'
    ]

    quarterly_users = (
        district_data.groupby(
            ['District', 'Year', 'Quarter']
        )['Registered_users']
        .max()
        .reset_index()
    )

    top_districts = (
        quarterly_users.groupby('District')[
            'Registered_users'
        ]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=top_districts,
        y='District',
        x='Registered_users',
        palette='magma'
    )

    plt.title(
        f'Top {top_n} Performing Districts',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Registered Users')
    plt.ylabel('District')

    plt.tight_layout()

    plt.show()


# 3. EMERGING GROWTH DISTRICTS

def plot_emerging_growth_districts(map_user, top_n=10):

    """
    Identify fast growing districts.
    """

    district_data = map_user[
        map_user['State'] != 'India'
    ]

    quarterly_users = (
        district_data.groupby(
            ['District', 'Year']
        )['Registered_users']
        .max()
        .reset_index()
    )

    growth = (
        quarterly_users.groupby('District')
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

    trend_data = quarterly_users[
        quarterly_users['District'].isin(
            top_growth['District']
        )
    ]

    plt.figure(figsize=(18, 8))

    sns.lineplot(
        data=trend_data,
        x='Year',
        y='Registered_users',
        hue='District',
        marker='o',
        linewidth=2.5
    )

    plt.title(
        'Emerging Growth Districts',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year')
    plt.ylabel('Registered Users')

    plt.legend(
        title='District',
        bbox_to_anchor=(1.02, 1),
        loc='upper left'
    )

    plt.tight_layout()

    plt.show()


# 4. ENGAGEMENT RATIO ANALYSIS

def plot_engagement_ratio_analysis(map_user, top_n=15):

    """
    Analyze App Opens per Registered User.
    """

    district_data = map_user[
        map_user['State'] != 'India'
    ]

    engagement = (
        district_data.groupby(
            ['District', 'Year', 'Quarter']
        )[
            ['Registered_users', 'App_opens']
        ]
        .max()
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
        engagement.groupby('District')[
            'Engagement_ratio'
        ]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=ratio,
        y='District',
        x='Engagement_ratio',
        palette='coolwarm'
    )

    plt.title(
        'Top Districts by Engagement Ratio',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('App Opens Per User')
    plt.ylabel('District')

    plt.tight_layout()

    plt.show()


# 5. STATE GROWTH HOTSPOTS

def plot_state_growth_hotspots(map_user):

    """
    Detect rapidly growing states.
    """

    state_data = map_user[
        map_user['State'] != 'India'
    ]

    quarterly_users = (
        state_data.groupby(
            ['State', 'Year']
        )['Registered_users']
        .max()
        .reset_index()
    )

    heatmap_data = quarterly_users.pivot_table(
        values='Registered_users',
        index='State',
        columns='Year',
        aggfunc='sum'
    )

    plt.figure(figsize=(16, 10))

    sns.heatmap(
        heatmap_data,
        cmap='YlGnBu'
    )

    plt.title(
        'State Growth Hotspots',
        fontsize=18,
        fontweight='bold'
    )

    plt.tight_layout()

    plt.show()

# 6. DISTRICT GROWTH HOTSPOTS

def plot_district_growth_hotspots(map_user, top_n=15):

    """
    Detect fastest growing districts.

    Growth % is calculated using:
    first year vs last year registered users.
    """
    district_data = map_user[
        map_user['State'] != 'India'
    ]

    yearly_users = (
        district_data.groupby(
            ['District', 'Year']
        )['Registered_users']
        .max()
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

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=growth,
        y='District',
        x='Growth_%',
        palette='rocket'
    )

    plt.title(
        f'Top {top_n} Regional Growth Hotspots',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Growth Percentage')
    plt.ylabel('District')

    plt.tight_layout()

    plt.show()