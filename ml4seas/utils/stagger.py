def stagger(data, nshift=3): 
    
    """
    function to stagger each column of a
    time-series dataframe 
    """
    
    cols = data.columns
    
    ldata = []
    
    for col in cols: 
        df = data.loc[:,[col]].copy()
        for ts in range(1, nshift+1): 
            dfs = df.loc[:,[col]].tshift(ts)
            dfs.columns = [f"{col}_{ts}"]
            df = pd.concat([df, dfs], axis=1)
        ldata.append(df)
    
    df = pd.concat(ldata, axis=1)
    
    return df.dropna(axis=0)
