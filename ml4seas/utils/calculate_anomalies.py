def calculate_anomalies(ts_series): 
    
    """
    given one Pandas Series containing seasonally aggregated values (Note: NOT a dataframe) 
    calculates the anomaly for each season 
    
    climatology by default is 1981 - 2010
    
    Parameters
    ----------
    
    - ts_series : a Pandas Series, with datetime index 
    
    Return
    ------
    
    - ts_series_anoms : Pandas Series with the corresponding anomalies 
    
    """
    
    def demean(x): 
        return x - x.loc['1981':'2010',].mean()
    
    ts_series_anoms = ts_series.groupby(ts_series.index.month).apply(demean) 
    
    ts_series_anoms = ts_series_anoms.sort_index()
    
    return ts_series_anoms
