# cenariostestespegasus/_bootstrap.py
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # sobe p/ raiz do projeto
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
