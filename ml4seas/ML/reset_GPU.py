def reset_GPU(): 
    """
    reset and clear memory of the GPU 
    """
    from numba import cuda
    device = cuda.get_current_device(); 
    device.reset()
