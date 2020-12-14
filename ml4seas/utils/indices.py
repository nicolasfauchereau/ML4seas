def calculate_NINO34(dset):
    
    nino = dset.sel(lat=slice(-5, 5), lon=slice((360 - 170), (360 - 120)))
    
    nino = nino.mean(['lat', 'lon'])
    
    return nino

def calculate_EMI(dset): 
    
    dom_A = dset.sel(lat=slice(-10., 10.), lon=slice(165., 220.)).mean(['lat','lon']) 
    
    dom_B = dset.sel(lat=slice(-15., 5.), lon=slice(250., 290.)).mean(['lat','lon']) 
    
    dom_C = dset.sel(lat=slice(-10., 20.), lon=slice(125., 145.)).mean(['lat','lon'])
    
    EMI = dom_A-0.5*dom_B-0.5*dom_C
    
    return EMI

def calculate_IOD(dset, dim='init'): 
    
    EAST = dset.sel(lon=slice(90, 110), lat=slice(-10,0)).mean('lat').mean('lon')
    WEST = dset.sel(lon=slice(50, 70), lat=slice(-10,10)).mean('lat').mean('lon')

    EAST = (EAST - EAST.mean(dim)) / EAST.std(dim)
    WEST = (WEST - WEST.mean(dim)) / WEST.std(dim)

    IOD = WEST - EAST  

    IOD.compute()

    return IOD 

def calculate_SPSD(dset, dim='init', var_name='sst', ensmean=True): 

    from scipy.stats import zscore

    if ensmean and 'member' in dset.dims: 

        dset = dset.mean('member')

    NW_pole = dset.sel(lat=slice(-50.,-35), lon=slice(170.,190.)).mean('lat').mean('lon')
    
    SE_pole = dset.sel(lat=slice(-57.5,-45.), lon=slice(220.,240.)).mean('lat').mean('lon')

    NW_pole = NW_pole.to_dataframe()[[var_name]]

    SE_pole = SE_pole.to_dataframe()[[var_name]]

    NW_pole = NW_pole.unstack()

    SE_pole = SE_pole.unstack() 

    NW_pole = NW_pole.apply(zscore)

    SE_pole = SE_pole.apply(zscore) 

    spsd = NW_pole - SE_pole

    spsd.columns = pd.MultiIndex.from_product([['SPSD'], range(spsd.shape[1])])

    return spsd

def calculate_SAM(dset, var_name='msl'): 
    
    s40 = dset.sel(lat=-40).mean('lon')
    s65 = dset.sel(lat=-65).mean('lon')

    s65 = s65[var_name].to_dataframe().drop('lat', axis=1).unstack()
    s40 = s40[var_name].to_dataframe().drop('lat', axis=1).unstack()

    def demean(x): 
        z = (x - x.loc['1981':'2010',:].mean()) / x.loc['1981':'2010',:].std() 
        return z
    
    s65 = s65.groupby(s65.index.month).apply(demean)

    s40 = s40.groupby(s40.index.month).apply(demean)

    SAM = s40 - s65

    return SAM

def calculate_M1(dset, var_name='msl'): 

    M1 = dsetm.sel(lat=-42.8821, lon=147.3272, method='nearest') - dsetm.sel(lat=-44.0058, lon=176.5401, method='nearest') - dsetm

    M1 = M1[var_name].to_dataframe().unstack()

    M1.columns = pd.MultiIndex.from_product([['M1'], range(M1.shape[1])])

    M1 = M1.groupby(M1.index.month).apply(demean)

    return M1

def calculate_Z1(dset, var_name='msl'): 

    Z1 = dsetm.sel(lat=-36.8483, lon=174.7625, method='nearest') - dsetm.sel(lat=-43.5320, lon=172.6397, method='nearest') - dsetm

    Z1 = Z1['msl'].to_dataframe().unstack()

    Z1.columns = pd.MultiIndex.from_product([['Z1'], range(Z1.shape[1])])

    Z1 = Z1.groupby(Z1.index.month).apply(demean)

    return M1

