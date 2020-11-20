def lag_df(df, max_lag=6, dropna=False): 
    """
    "create extraneous columns in a dataframe, containing lagged version 
    of the original columns, up to paraneter `max_lag`"

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe with the columns to lag
    max_lag : int, optional
        The maximum number of lags, by default 6
    dropna : bool, optional
        whether or not to drop the missing values in the resulting dataframe, by default False

    Returns
    -------
    pandas.DataFrame
        The resulting dataframe, with the resulting columns having the
        suffix '_{i}' (with i = 0 to `max_lag - 1`) appended to the name of each column
    """
    import pandas as pd 
    import numpy as np

    df_lagged = pd.concat(
    [df.shift(i).add_suffix(f"_{i}") for i in range(max_lag)], axis=1
    )
    
    if dropna: 
        
        df_lagged = df_lagged.dropna()
    
    return df_lagged