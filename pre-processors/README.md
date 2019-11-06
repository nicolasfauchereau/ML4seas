This part of the pipeline does the GCMs (and ERA reanalysis) outputs **pre-processing**, i.e.: 

+ harmonize variables names, dimension names, conventions
+ regrid all the model (+ reanalyses) on a common regular grid, using bilinear interpolation via the [xesmf](https://xesmf.readthedocs.io/en/latest/) package
