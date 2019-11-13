This part of the pipeline does the GCMs (and ERA reanalysis) outputs **pre-processing**, i.e.: 

+ converts from grib to netcdf 
+ concatenate files 
+ harmonize variables names, dimension names, conventions
+ regrid all the model (+ reanalyses) on a common regular grid, using bilinear interpolation via the [xesmf](https://xesmf.readthedocs.io/en/latest/) package
+ etc ... 

i.e. all the steps necessary to have the different GCM outputs compatible so that the processing and model building steps of the pipeline do not need to *know* what GCM its inputs are coming from 
