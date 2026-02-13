import sys
from pathlib import Path


f = Path(__file__).parent.parent
sys.path.insert(0, str(f))