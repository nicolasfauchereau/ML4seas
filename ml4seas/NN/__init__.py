try: 
    from .XrDataGenerator import XrDataGenerator
    from .PeriodicPadding2D import PeriodicPadding2D
    from .PrunePeriodicPadding2D import PrunePeriodicPadding2D 
    from .ResizeLayer import ResizeLayer
    from .PeriodicConv2D import PeriodicConv2D
except ImportError as e:
    pass