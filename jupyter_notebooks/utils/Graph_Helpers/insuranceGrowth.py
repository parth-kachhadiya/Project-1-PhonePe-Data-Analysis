import matplotlib.pyplot as plt
import seaborn as sns

"""
IMPORTANT:

1. Transaction_type column in Aggregated_insurance
   contains only 'Insurance' values.

   Therefore:
   -> Ignore Transaction_type column completely.

2. Transaction_count and Transaction_amount
   are additive metrics.

   Therefore:
   -> use SUM()

3. Rows where State == 'India'
   represent overall country performance.
"""

# 1. INSURANCE TRANSACTION GROWTH

def plot_insurance_transaction_growth(agg_insurance):

    """
    Analyze insurance transaction growth over time.

    - X-axis = Years
    - Each line = Quarter
    """

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

    plt.figure(figsize=(14, 7))

    sns.lineplot(
        data=trend,
        x='Year',
        y='Transaction_count',
        hue='Quarter',
        marker='o',
        linewidth=3,
        palette='Set1'
    )

    plt.title(
        'Insurance Transaction Growth Trend',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year')
    plt.ylabel('Transaction Count')

    plt.xticks(
        sorted(trend['Year'].unique())
    )

    plt.legend(title='Quarter')

    plt.tight_layout()

    plt.show()


# 2. INSURANCE AMOUNT GROWTH

def plot_insurance_amount_growth(agg_insurance):

    """
    Analyze insurance transaction amount growth.
    """

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

    plt.figure(figsize=(14, 7))

    sns.lineplot(
        data=trend,
        x='Year',
        y='Transaction_amount',
        hue='Quarter',
        marker='o',
        linewidth=3,
        palette='Set2'
    )

    plt.title(
        'Insurance Transaction Amount Growth',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year')
    plt.ylabel('Transaction Amount')

    plt.xticks(
        sorted(trend['Year'].unique())
    )

    plt.legend(title='Quarter')

    plt.tight_layout()

    plt.show()


# 3. INSURANCE ATV ANALYSIS

def plot_insurance_atv_analysis(map_insurance, top_n=15):

    """
    Analyze Average Insurance Transaction Value
    across states.

    ATV = Amount / Count
    """

    state_data = map_insurance[
        map_insurance['State'] != 'India'
    ]

    atv = (
        state_data.groupby('State')[
            ['Transaction_amount', 'Transaction_count']
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

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=atv,
        y='State',
        x='ATV',
        palette='rocket'
    )

    plt.title(
        'Insurance Average Transaction Value',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Average Transaction Value')
    plt.ylabel('State')

    plt.tight_layout()

    plt.show()


# 4. STATE INSURANCE PENETRATION

def plot_state_insurance_penetration(map_insurance, top_n=15):

    """
    Identify states with strongest
    insurance adoption.
    """
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

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=penetration,
        y='State',
        x='Transaction_count',
        palette='viridis'
    )

    plt.title(
        f'Top {top_n} Insurance Adoption States',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Transaction Count')
    plt.ylabel('State')

    plt.tight_layout()

    plt.show()


# 5. DISTRICT INSURANCE PENETRATION

def plot_district_insurance_penetration(map_insurance, top_n=15):

    """
    Identify districts with strongest
    insurance adoption.
    """

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

    plt.figure(figsize=(14, 8))

    sns.barplot(
        data=penetration,
        y='District',
        x='Transaction_count',
        palette='magma'
    )

    plt.title(
        f'Top {top_n} Insurance Adoption Districts',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Transaction Count')
    plt.ylabel('District')

    plt.tight_layout()

    plt.show()


# 6. HOT QUARTER OF BUYING INSURANCE

def plot_hot_quarter_insurance(agg_insurance):

    """
    Identify hottest insurance buying quarter.
    """

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

    plt.figure(figsize=(14, 7))

    sns.barplot(
        data=quarter_data,
        x='Year',
        y='Transaction_count',
        hue='Quarter',
        palette='Set2'
    )

    plt.title(
        'Hot Quarter of Buying Insurance',
        fontsize=18,
        fontweight='bold'
    )

    plt.xlabel('Year')
    plt.ylabel('Transaction Count')

    plt.legend(title='Quarter')

    plt.tight_layout()

    plt.show()
