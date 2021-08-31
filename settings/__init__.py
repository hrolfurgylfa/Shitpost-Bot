from .settings import *
from .keys import *

try:
    from .local import *
except ImportError:
    pass
