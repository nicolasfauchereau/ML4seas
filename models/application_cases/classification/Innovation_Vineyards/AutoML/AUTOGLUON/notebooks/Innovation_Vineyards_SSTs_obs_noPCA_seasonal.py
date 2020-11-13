#!/home/nicolasf/anaconda3/envs/autogluon-gpu/bin/python

# Parameters 

application = 'Innovation_Vineyards'
varname = 'TMEAN_N'
stat = 'mean'
num_quantiles = 3
target_type = f'cat{num_quantiles}'
step = 4
lag_sst = True
max_lag = 6
detrend_sst = False

# imports 
import pathlib
import pickle

import numpy as np 
import pandas as pd 
import xarray as xr

# import autogluon 
from autogluon import TabularPrediction as task

HOME = pathlib.Path.home()
CWD = pathlib.Path.cwd()

# ### read the target variable 

ipath_target = pathlib.Path(HOME.joinpath(f"research/Smart_Ideas/outputs/targets/application_cases/{application}/SEASONAL/{varname}"))


target = pd.read_csv(ipath_target.joinpath(f"Seasonal_{varname}_{stat}_anomalies_and_Q{num_quantiles}_categories.csv"), index_col=0, parse_dates=True)


target = target.loc[:,[target_type]]


# ### keep only data post 1981 to enable direct comparison with GCM derived fields 

target = target.loc['1981':,:]


ipath_sst = pathlib.Path(HOME.joinpath("/media/nicolasf/END19101/data/ERSST/processed"))

lfiles_sst = list(ipath_sst.glob("*.nc")) 

lfiles_sst.sort() 

dset_sst = xr.open_mfdataset(lfiles_sst, concat_dim='time')

dset_sst = dset_sst.sel(time=slice('1981',None))


# ### domain selection 

domain_def = {}
domain_def['HB_seasonal'] = [120, 290, -60, 40]
domain_def['local'] = [150, 200, -50, -10]
domain_def['regional'] = [90, 300, -65, 50]
domain_def['ext_regional'] = [70, 300, -70, 60]
domain_def['global'] = [0, 360, -70, 70]
domain_def['tropics'] = [0, 360, -40, 40]

domain = 'HB_seasonal'

dset_sst = dset_sst.sel(lat=slice(*domain_def[domain][2:]), lon=slice(*domain_def[domain][:2])) 

dset_sst_shift = dset_sst.copy()

dset_sst_shift = dset_sst.shift(time=step)

dset_sst_shift = dset_sst_shift.isel(time=slice(step, None))

dset_sst_shift = dset_sst_shift.stack(s=('lat','lon'))

dset_sst_shift = dset_sst_shift.dropna('s')

dset_sst_shift.load()

sst_data = dset_sst_shift['sst'].data

df_sst = pd.DataFrame(sst_data, index=dset_sst_shift.time.to_index())

if detrend_sst: 
    df_sst = df_sst.apply(detrend)

if lag_sst: 
    dset_lagged = pd.concat(
    [df_sst.shift(i).add_suffix(f"_{i}") for i in range(max_lag)], axis=1
    )
    dset_lagged = dset_lagged.dropna()
    df_sst = dset_lagged

target.index.freq = 'M'

df = pd.concat([df_sst, target], axis=1)

df = df.dropna(axis=0)

saved_models = pathlib.Path('./saved_models/AUTOGLUON_v3/')

seasonal_acc = {}
seasonal_best_model = {}
seasonal_predictor_info = {}

for random_state in range(10): 

    for season in range(1, 13): 

        print(f"\ntraining and evaluating for season {season}")
        
        dfs = df.loc[df.index.month == season]
        
        opath = saved_models.joinpath(f'./autogluon_exp_SKPCA_SSTobs_1981_2010_pred_{application}_reg_{varname}_targetvar_{target_type}_target_type_season_{season}')
        
        if not opath.exists(): 
            opath.mkdir(parents=True)
        
        dfs = dfs.sample(frac=1., random_state=random_state)
        
        predictor = task.fit(train_data=dfs, label=target_type, auto_stack=True, presets='best_quality', output_directory=opath, verbosity=0)
        
        seasonal_acc[season] = predictor.model_performance[predictor.get_model_best()]
        
        seasonal_best_model = predictor.get_model_best()
        
        seasonal_predictor_info[season] = predictor.info()
        
        print(f"best model is {predictor.get_model_best()}, validation accuracy reaching {predictor.model_performance[predictor.get_model_best()]}")

    pd.Series(seasonal_acc).to_csv(f"seasonal_ACC_{application}_{varname}_{target_type}_SSTobs_no_PCA_lagged_{max_lag}m_randomstate_{random_state}.csv")

    with open(f"seasonal_predinfo_{application}_{varname}_{target_type}_SSTobs_no_PCA_lagged_{max_lag}m_randomstate_{random_state}.pkl",'wb') as f: 
        pickle.dump(seasonal_best_model, f)