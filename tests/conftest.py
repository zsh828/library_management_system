import sys
import os

# Add the project root directory to the Python path to ensure 'src' can be imported
# regardless of the current working directory during test collection.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))