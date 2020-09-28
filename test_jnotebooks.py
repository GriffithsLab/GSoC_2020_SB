import subprocess
import tempfile
import os

def _exec_notebook(path):
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=None",
                "--output", fout.name, path]
        subprocess.check_call(args)


def test():
  _exec_notebook('Example1_CentralPeak.ipynb')
  _exec_notebook('Example2_Band_Peak_Power.ipynb')
  _exec_notebook('Example3_CorrelationCoefficient.ipynb')


#name_examples = os.listdir('examples')
#  for ex in name_examples:
 #   _exec_notebook('examples/'+ex)
    
"""Option 2"""
#  jupyter nbconvert --ExecutePreprocessor.timeout=1000 --to notebook --execute examples/Example1_CentralPeak.ipynb
