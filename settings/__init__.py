import os

_ENV_VAR = "ZOMIC"
_PRODUCTION = "PRODUCTION"
_LOCAL = "LOCAL"

from .base import *

if os.environ.get(_ENV_VAR) == _PRODUCTION:
    from .production import *
elif os.environ.get(_ENV_VAR) == _LOCAL:
    from .local import *
