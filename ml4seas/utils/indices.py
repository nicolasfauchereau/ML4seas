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