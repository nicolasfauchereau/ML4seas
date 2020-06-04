def calculate_quantile(ts_series, quant_values): 
    
    """
    given one Pandas Series containing seasonally aggregated values (Note: NOT a dataframe) 
    and a list of quantiles, calculates the quantile category for each season 
    
    climatology by default is 1981 - 2010
    
    Parameters
    ----------
    
    - ts_series : a Pandas Series, with datetime index 
    - quant_values : a list of quantiles (e.g. [0.3333, 0.66666] for terciles)
    
    Return
    ------
    
    - ts_series_cat : a Pandas Series with the corresponding category 
    
    """
    
    ts_series_cat = []
    
    quantiles_list = []

    for month in range(1, 13):

        ts_series_m = ts_series[ts_series.index.month == month]

        clim = ts_series_m.loc['1981':'2010']

        quantiles = [clim.quantile(q=q) for q in quant_values.tolist()]

        quantiles_list.append(quantiles.copy())

        quantiles.insert(0, -np.inf)

        quantiles.append(np.inf)

        ts_series_m_cats = pd.cut(ts_series_m, quantiles, labels=list(range(1, num_quantiles + 1)))

        ts_series_cat.append(ts_series_m_cats)

        del(quantiles) 
        
    ts_series_cat = pd.concat(ts_series_cat)
    
    ts_series_cat = ts_series_cat.sort_index()
    
    return ts_series_cat 
