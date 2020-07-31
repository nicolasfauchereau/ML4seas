import numpy as np
import tensorflow as tf

def xarray_to_TF_record(dset, varname='t2m', opath=None, fname=None):
    """
    """
    data = dset[varname].data
    data_tensor = tf.convert_to_tensor(data, np.float32)
    s_tensor = tf.io.serialize_tensor(data_tensor) 
    tf.io.write_file(str(opath / fname), s_tensor)
    dset.close()  
