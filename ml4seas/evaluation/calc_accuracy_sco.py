def calc_accuracy_sco(df, tolerance=True): 
    
    """
    calculates the 'SCO' accuracy, which 'optionally' allows for a 5% tolerance
    
    Arguments
    ---------
    
    df : the pandas DataFrame containing 4 columns: 
    
        0: the observed category from 1 to n categories
        1: the probability in percentage (0 to 100) for the first category
        2: the probability in percentage (0 to 100) for the first category
        3: the probability in percentage (0 to 100) for the first category
        ...  
        
    tolerance : Boolean, whether or not to turn the tolerance on 
    
    Return
    ------
    
    acc : the accuracy from 0 to 1 
    
    
    """

    import numpy as np 
    import pandas as pd

    acc = []
    for i in range(len(df)):
        if tolerance: 
            r = (int(df.iloc[i,0]) == df.iloc[i,1:].argmax()) or ((df.iloc[i, df.iloc[i,1:].argmax()] - df.iloc[i,int(df.iloc[i,0])]) <= 5.)
        else: 
            r = (int(df.iloc[i,0]) == df.iloc[i,1:].argmax())
        acc.append(r)
    acc = np.array(acc)
    return acc.sum() / len(acc)

