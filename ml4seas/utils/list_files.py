def list_files(dpath, pattern=None, extension=".nc", include=None, exclude=None, verbose=0): 
    """
    list_files list files in a folder according to patterns

    Parameters
    ----------
    dpath : string or pathlib.Path
        The path to the files (str)
    pattern : str, optional
        The pattern to follow, by default None
    extension : str, optional
        the extension, by default ".nc"
    include : str, optional
        a string that the items in the list must contain, by default None
    exclude : str, optional
        a string that the items in the list must contain, by default None
    verbose : int, optional
        whether or not to output some diagnostics, by default 0

    Returns
    -------
    list
        The sorted list of files
"""
    import pathlib 

    if not isinstance(dpath, pathlib.PosixPath): 
        dpath = pathlib.Path(dpath)

    lfiles = list(dpath.glob(f"{pattern}{extension}"))

    if len(lfiles) == 0: 
        raise ValueError("No files in list")
    else: 
        if include is not None: 
            lfiles = [x for x in lfiles if include in str(x)]
        if exclude is not None: 
            lfiles = [x for x in lfiles if exclude not in str(x)]

    lfiles.sort() 

    if verbose == 1:
        print(f"loaded files, list length {len(lfiles)}")
        print(f"the first file is {str(lfiles[0])}")
        print(f"the last file is {str(lfiles[-1])}")

    return lfiles
