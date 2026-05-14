import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# HANDLE MISSING APP OPENS

def handle_missing_app_opens(map_user):

    """
    App_opens = 0 from:
    2018-Q1 to 2019-Q1

    These are missing values,
    NOT actual zero engagement.
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


"""
IMPORTANT:

1. map_user DOES NOT contain repeated totals.

Therefore:

Registered_users -> SUM()
App_opens        -> SUM()

2. App_opens = 0
from 2018-Q1 to 2019-Q1
means missing values.

3. map_map metrics are additive.

Therefore:

Transaction_count  -> SUM()
Transaction_amount -> SUM()

4. Exclude India rows
for regional strategic analysis.
"""

# 1. POTENTIAL USER SEGMENTS

def plot_potential_user_segments(map_user, top_n=15):

    """
    Identify districts with:
    - high registered users
    - low engagement

    These are potential reactivation regions.
    """

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

    engagement['App_Opens_Per_User'] = (
        engagement['App_opens']
        /
        engagement['Registered_users']
    )

    engagement = (
        engagement.sort_values(
            by=['Registered_users', 'App_Opens_Per_User'],
            ascending=[False, True]
        )
        .head(top_n)
    )

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=engagement,
        y='District',
        x='Registered_users',
        palette='flare'
    )

    plt.title(
        'Potential User Segments (High Users, Low Engagement)',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Registered Users')
    plt.ylabel('District')

    plt.tight_layout()

    plt.show()


# 2. POTENTIAL GROWTH REGIONS

def plot_potential_growth_regions(map_user, top_n=15):

    """
    Identify low-adoption but fast-growing districts.
    """

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

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=growth,
        y='District',
        x='Growth_%',
        palette='crest'
    )

    plt.title(
        'Potential Growth Regions',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Growth Percentage')
    plt.ylabel('District')

    plt.tight_layout()

    plt.show()


# 3. GROWTH OPPORTUNITY REGIONS

def plot_growth_opportunity_regions(map_user, top_n=15):

    """
    Identify high-growth low-adoption regions.
    """

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
            Current_Users=('Registered_users', 'last'),
            First_Users=('Registered_users', 'first')
        )
        .reset_index()
    )

    growth = growth[
        growth['First_Users'] > 0
    ]

    growth['Growth_%'] = (
        (
            growth['Current_Users']
            -
            growth['First_Users']
        )
        /
        growth['First_Users']
    ) * 100

    opportunity = (
        growth.sort_values(
            by=['Growth_%', 'Current_Users'],
            ascending=[False, True]
        )
        .head(top_n)
    )

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=opportunity,
        y='District',
        x='Growth_%',
        palette='crest'
    )

    plt.title(
        'Potential Growth Opportunity Regions',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Growth Percentage')
    plt.ylabel('District')

    plt.tight_layout()

    plt.show()


# 4. UNUSUAL TRANSACTION PATTERN DETECTION

def plot_unusual_transaction_patterns(map_map):

    """
    Detect abnormal transaction behavior
    using boxplot.
    """

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
        txn.groupby('State')['Transaction_amount']
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .index
    )

    txn = txn[
        txn['State'].isin(top_states)
    ]

    plt.figure(figsize=(18, 8))

    sns.boxplot(
        data=txn,
        x='State',
        y='Transaction_amount',
        palette='Set3'
    )

    plt.title(
        'Unusual Transaction Pattern Detection',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('State')
    plt.ylabel('Transaction Amount')

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

