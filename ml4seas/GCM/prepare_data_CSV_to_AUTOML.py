def prepare_data_CSV_to_AUTOML(data, gcm_index=-13, GCM='All', region_name=None, target_type=None, scaling=True, doPCA=True, n_components=0.9): 
    """
    Small function that prepares the data initially contained in the 
    processed CSV files for ingestion into PyCARET
    
    Arguments
    --------- 
    
    - gcm_index : negative index (always) indicating what 
            is the last column containing the predictor variable 
            default is -12 for the 'ext_regional' geographical 
            domain 
    - GCM: 'All' or specific GCM in ['CMCC', 'CanCM4i', 'CanSIPSv2', 
                                    'DWD', 'ECMWF', 'GEM_NEMO', 'JMA',
                                    'METEO_FRANCE', 'NASA_GEOSS2S', 'NCEP_CFSv2', 'UKMO']
    - region_name : ['NNI','WNI','ENI','NSI','WSI','ESI']
    - target_type : 'cat3_category' or 'anomalies'
    
    Return
    ------
    
    - data : the data filtered by GCM (if not 'All'), region_name and target type 
    - GCM_index: the GCMs index 

    """
    
    import numpy as np 
    import pandas as pd 
    from sklearn.preprocessing import  StandardScaler 
    from sklearn.decomposition import PCA

    # extract one GCM if not 'All'
    if GCM != 'All': 
        data = data.query(f"GCM == '{GCM}'") 
    
    # GCM name and associated index
    GCMs_name = data.loc[:,['GCM']]  
    
    # GCM (features)
    GCM_data = data.iloc[:,0:gcm_index]
    
    # associated index
    index = GCM_data.index
    
    # associated column names 
    cols = GCM_data.columns

    # target variable 
    target = data.loc[:,[f'{region_name}_{target_type}']]
    
    # get the values for X 
    X = GCM_data.values
    
    if scaling:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    else: 
        scaler = None
    
    if doPCA: 
        pca = PCA(n_components=n_components)
        pca = pca.fit(X)
        X = pca.transform(X)
        npcs = X.shape[1]
    else: 
        pca = None

    # now casts X into a DataFrame
    if doPCA: 
        df = pd.DataFrame(X, index=index, columns=[f"PC{i}" for i in range(1, npcs+1)])
    else: 
        df = pd.DataFrame(GCM_data.values, index=index, columns=cols)
        
    # add the target variable 
    data = pd.concat([df, target], axis=1)
    
    return data, GCMs_name, scaler, pca
