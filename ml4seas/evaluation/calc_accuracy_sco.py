def calc_accuracy_sco(df, tolerance=True): 

    import numpy as np 
    import pandas as pd

    acc = []
    for i in range(len(df)):
        if tolerance: 
            r = df.iloc[i, df.iloc[i,0]] == df.iloc[i,1:].max() \
            or abs(df.iloc[i, df.iloc[i,0]]  - df.iloc[i,1:].max()) <= 5
        else: 
            r = df.iloc[i, df.iloc[i,0]] == df.iloc[i,1:].max()
        acc.append(r)
    acc = np.array(acc)
    return acc.sum() / len(acc)

