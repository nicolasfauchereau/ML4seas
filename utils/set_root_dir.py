def set_root_dir(root='local'): 
    """
    set the root directory all the way to the `data` directory
    
    valid options are: 
    
    - 'local'
    - 'gdata'
    - 'network' (for the network drive, please note that now the END19101 has been 
    transfered to the Hamilton drive, with ID hamwfs03)

    """
    
    import pathlib
    if root == 'local': 
        root_dir = pathlib.Path.home() / 'research' / 'Smart_Ideas' / 'data'
    elif root == 'gdata': 
        root_dir = pathlib.Path('/media/nicolasf/GDATA/END19101/Working/data/')
    elif root == 'network': 
        root_dir = pathlib.Path.home() / 'drives' / 'auck_projects' / 'END19101' / 'Working' / 'data'
    else: 
        print("invalid value for `root`, needs to be ['local','gdata','network']")
    return root_dir
