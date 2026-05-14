import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PREPROCESSING
def preprocess_data(df):

    df['Year_Quarter'] = (
        df['Year'].astype(str)
        + '-Q' +
        df['Quarter'].astype(str)
    )

    return df

agg_user = preprocess_data(agg_user)
agg_txn = preprocess_data(agg_txn)

def plot_india_user_growth(agg_user):

    """
    Analyze yearly registered user growth in India.

    IMPORTANT:
    Registered_users values are repeated for every User_brand
    within the same quarter.

    Therefore:
    - use MAX instead of SUM
    """

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

    plt.figure(figsize=(14, 7))

    sns.lineplot(
        data=yearly_users,
        x='Year',
        y='Registered_users',
        marker='o',
        linewidth=3,
        color='royalblue'
    )

    plt.title(
        'India Registered User Growth Over Years',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year')
    plt.ylabel('Registered Users')

    plt.xticks(
        sorted(yearly_users['Year'].unique())
    )

    plt.tight_layout()

    plt.show()

# 2. TOP STATES USER GROWTH COMPARISON

def plot_top_states_user_growth(agg_user, top_n=10):

    """
    Analyze yearly user growth for top states.

    IMPORTANT:
    Registered_users values are repeated for every User_brand
    within the same quarter.

    Therefore:
    - use MAX instead of SUM
    """

    state_users = agg_user[
        agg_user['State'] != 'India'
    ]

    quarterly_users = (
        state_users.groupby(
            ['State', 'Year', 'Quarter']
        )['Registered_users']
        .max()
        .reset_index()
    )

    top_states = (
        quarterly_users.groupby('State')['Registered_users']
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )

    filtered = quarterly_users[
        quarterly_users['State'].isin(top_states)
    ]

    yearly_trend = (
        filtered.groupby(
            ['Year', 'State']
        )['Registered_users']
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(18, 8))

    sns.lineplot(
        data=yearly_trend,
        x='Year',
        y='Registered_users',
        hue='State',
        marker='o',
        linewidth=2.5
    )

    plt.title(
        f'Top {top_n} States User Growth Over Years',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year')
    plt.ylabel('Registered Users')

    plt.xticks(
        sorted(yearly_trend['Year'].unique())
    )

    plt.legend(
        title='State',
        bbox_to_anchor=(1.02, 1),
        loc='upper left'
    )

    plt.tight_layout()

    plt.show()

# 3. TRANSACTION GROWTH TREND

def plot_transaction_growth(agg_txn):

    """
    Transaction growth trend where:
    
    - X-axis = Years
    - Each line = Quarter
    - Separate subplots for:
        1. Transaction Count
        2. Transaction Amount
    """

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

    fig, axes = plt.subplots(
        1, 2,
        figsize=(18, 7)
    )

    sns.lineplot(
        data=trend,
        x='Year',
        y='Transaction_count',
        hue='Quarter',
        palette='Set1',
        marker='o',
        linewidth=3,
        ax=axes[0]
    )

    axes[0].set_title(
        'Transaction Count Growth by Quarter',
        fontsize=16,
        fontweight='bold'
    )

    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Transaction Count')

    axes[0].legend(
        title='Quarter'
    )

    sns.lineplot(
        data=trend,
        x='Year',
        y='Transaction_amount',
        hue='Quarter',
        palette='Set2',
        marker='o',
        linewidth=3,
        ax=axes[1]
    )

    axes[1].set_title(
        'Transaction Amount Growth by Quarter',
        fontsize=16,
        fontweight='bold'
    )

    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Transaction Amount')

    axes[1].legend(
        title='Quarter'
    )

    plt.suptitle(
        'PhonePe Transaction Growth Trend',
        fontsize=20,
        fontweight='bold'
    )

    plt.tight_layout()

    plt.show()

# 4. YEAR-OVER-YEAR (YoY) GROWTH ANALYSIS

def plot_yoy_growth_analysis(agg_user, agg_txn):

    """
    Analyze YoY growth for users and transactions.
    Uses India rows only.
    """

    india_users = agg_user[
        agg_user['State'] == 'India'
    ]

    user_yearly = (
        india_users.groupby('Year')['Registered_users']
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

    yoy_df.set_index('Year').plot(
        kind='bar',
        figsize=(14, 7),
        color=['royalblue', 'seagreen']
    )

    plt.title(
        'Year-over-Year (YoY) Growth Analysis',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year')
    plt.ylabel('Growth Percentage')

    plt.xticks(rotation=0)

    plt.legend([
        'User Growth %',
        'Transaction Growth %'
    ])

    plt.tight_layout()
    plt.show()

# 5. QUARTER-OVER-QUARTER USER GROWTH

def plot_qoq_user_growth(agg_user):

    """
    Analyze QoQ user growth correctly.

    IMPORTANT:
    Registered_users values repeat for every User_brand.
    """
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

    plt.figure(figsize=(16, 7))

    sns.barplot(
        data=quarterly_users,
        x='Year_Quarter',
        y='QoQ_Growth_%',
        palette='Blues_r'
    )

    plt.title(
        'Quarter-over-Quarter User Growth',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year Quarter')
    plt.ylabel('Growth Percentage')

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

def plot_qoq_transaction_growth(agg_txn):

    """
    Analyze Quarter-over-Quarter transaction growth.
    Uses India rows only.
    """

    india_txn = agg_txn[
        agg_txn['State'] == 'India'
    ]

    quarterly = (
        india_txn.groupby('Year_Quarter')['Transaction_amount']
        .sum()
        .reset_index()
    )

    quarterly['QoQ_Growth_%'] = (
        quarterly['Transaction_amount']
        .pct_change() * 100
    )

    plt.figure(figsize=(16, 7))

    sns.barplot(
        data=quarterly,
        x='Year_Quarter',
        y='QoQ_Growth_%',
        palette='Greens_r'
    )

    plt.title(
        'Quarter-over-Quarter Transaction Growth',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year Quarter')
    plt.ylabel('Growth Percentage')

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()