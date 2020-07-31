# functions to serialise a bunch of netcdf files (read from disk)
# to Tensorflow TensorSlices and serialize to disk 

import pathlib

import numpy as np
import xarray as xr
import tensorflow as tf


def netcdf_to_TF_records(ipath=None, file_pattern = "*.nc", length=None, selfunc=None, varname = 't2m', opath=None): 
    """
    Parameters
    ----------
    ipath : path to the netcdf files 

    file_pattern : the file pattern (default is "*.nc")

    length : where to stop in the list (e.g. for train vs test)

    selfunc : a function to select or otherwise preprocess each file, e.g. 
        `
        def selfunc(dset): 
            dset = dset.sel(step=3).mean('member')
            return dset
        `
        can also include a scikit-learn (trained on a subset) 

        see train_scaler in ML 

    Return
    ------

    Nothing, but creates, a set of tf.load-able file.
    """
    # check the path, and create the paths
    def check_and_create_path(path): 
 
        if not isinstance(path, pathlib.PosixPath): 
            path = pathlib.Path(path)
        
        if not path.exists(): 
            path.mkdir(parents=True)

    check_and_create_path(ipath)
    check_and_create_path(opath)

    # list the files 
    lfiles = list(ipath.glob(file_pattern)) 
    lfiles.sort()

    if len(lfiles) == 0: 
        raise ValueError(f"seems there are no files in {str(ipath)}")
        pass
    else:
        if length is not None and length<len(lfiles):
            lfiles=lfiles[:length]
        for fname in lfiles: 
            dset = xr.open_dataset(fname)
            if selfunc is not None: 
                dset = selfunc(dset)
            data = dset[varname].data
            data_tensor = tf.convert_to_tensor(data, np.float32)
            s_tensor = tf.io.serialize_tensor(data_tensor) 
            tf.io.write_file(str(opath / fname.replace(".nc",".tfd")), s_tensor)
            dset.close() 
            




