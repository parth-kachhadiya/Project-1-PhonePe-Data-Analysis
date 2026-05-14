import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

agg_user = pd.read_csv("Aggregated_user.csv")
agg_txn = pd.read_csv("Aggregated_transaction.csv")

def add_year_quarter(df):

    """
    Create Year_Quarter column.
    """

    df['Year_Quarter'] = (
        df['Year'].astype(str)
        + '-Q' +
        df['Quarter'].astype(str)
    )

    return df

agg_user = add_year_quarter(agg_user)
agg_txn = add_year_quarter(agg_txn)

# 1. TRANSACTION TYPE ANALYSIS

def plot_transaction_type_analysis(agg_txn):

    """
    Analyze dominant transaction categories in PhonePe.
    
    Uses:
    - India rows only
    - Transaction Amount aggregation
    """
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

    plt.figure(figsize=(14, 7))

    sns.barplot(
        data=txn_type,
        y='Transaction_type',
        x='Transaction_amount',
        palette='viridis'
    )

    plt.title(
        'Transaction Type Analysis',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Transaction Amount')
    plt.ylabel('Transaction Type')

    plt.tight_layout()

    plt.show()


# 2. ATV ANALYSIS BY TRANSACTION TYPE

def plot_atv_by_transaction_type(agg_txn):

    """
    Analyze Average Transaction Value (ATV)
    across transaction categories.
    
    ATV = Transaction Amount / Transaction Count
    """

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
        atv_data['Transaction_amount'] /
        atv_data['Transaction_count']
    )

    atv_data = atv_data.sort_values(
        by='ATV',
        ascending=False
    )

    plt.figure(figsize=(14, 7))

    sns.barplot(
        data=atv_data,
        x='Transaction_type',
        y='ATV',
        palette='magma'
    )

    plt.title(
        'Average Transaction Value by Transaction Type',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Transaction Type')
    plt.ylabel('Average Transaction Value')

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.show()


# 3. ATV ANALYSIS BY STATE

def plot_atv_by_state(agg_txn, top_n=15):

    """
    Compare Average Transaction Value across states.
    
    Excludes India rows.
    """

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
        atv_state['Transaction_amount'] /
        atv_state['Transaction_count']
    )

    atv_state = (
        atv_state.sort_values(
            by='ATV',
            ascending=False
        )
        .head(top_n)
    )

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=atv_state,
        y='State',
        x='ATV',
        palette='coolwarm'
    )

    plt.title(
        f'Top {top_n} States by Average Transaction Value',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Average Transaction Value')
    plt.ylabel('State')

    plt.tight_layout()

    plt.show()


# 4. SMARTPHONE ECOSYSTEM ANALYSIS


def plot_smartphone_ecosystem(agg_user, top_n=10):

    """
    Analyze dominant smartphone brands among PhonePe users.
    
    Uses:
    - India rows only
    - User_count aggregation
    """

    india_users = agg_user[
        agg_user['State'] == 'India'
    ]

    brands = (
        india_users.groupby('User_brand')[
            'User_count'
        ]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    plt.figure(figsize=(14, 7))

    sns.barplot(
        data=brands,
        x='User_brand',
        y='User_count',
        palette='Set2'
    )

    plt.title(
        'Smartphone Ecosystem Analysis',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Smartphone Brand')
    plt.ylabel('User Count')

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.show()


# 5. USER ENGAGEMENT PATTERN ANALYSIS

def plot_user_engagement_trend(agg_user):

    """
    Analyze quarter-wise user engagement trend.

    IMPORTANT:
    App_opens values repeat for every User_brand.
    
    Therefore:
    - use MAX instead of SUM
    """

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

    plt.figure(figsize=(14, 7))

    sns.lineplot(
        data=engagement,
        x='Year',
        y='App_opens',
        hue='Quarter',
        marker='o',
        linewidth=3,
        palette='Set1'
    )

    plt.title(
        'Quarter-wise User Engagement Trend',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year')
    plt.ylabel('App Opens')

    plt.xticks(
        sorted(engagement['Year'].unique())
    )

    plt.legend(title='Quarter')

    plt.tight_layout()

    plt.show()
