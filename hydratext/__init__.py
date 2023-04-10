"""Module for HydraText."""

__version__ = "1.0"


import os



import sys
from streamlit.web import cli as stcli
import subprocess

# Get the directory where the current file is located

# Run a command that takes the current file as the location

def hydratext():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    command = f"streamlit run {current_dir}/HydraText.py"
    os.system(command)
    print(subprocess.run("pwd"))
    sys.argv = ["streamlit", "run", "HydraText.py"]
    sys.exit(stcli.main())