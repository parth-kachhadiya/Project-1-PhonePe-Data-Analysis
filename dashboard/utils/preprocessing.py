import numpy as np
import pandas as pd

# =========================================================
# PREPROCESSING
# =========================================================


def preprocess_data(df):

    df['Year_Quarter'] = (
        df['Year'].astype(str)
        + '-Q' +
        df['Quarter'].astype(str)
    )

    return df


# =========================================================
# HANDLE MISSING APP OPENS
# =========================================================


def handle_missing_app_opens(map_user):

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