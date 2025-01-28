import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from api_gateway.main import app

__all__ = ["app"]
