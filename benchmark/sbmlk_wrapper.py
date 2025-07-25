# sbmlk_wrapper.py
from SBMLKinetics.kinetics_classification import _dataSetStatistics  # wherever the function is

import os
import tempfile
import shutil
import time
import zipfile

def run_sbmlk_on_file(sbml_path: str):
    """
    Runs SBMLKinetics classification on a single SBML file.
    Returns a dict: { 'time': float, 'classification': DataFrame, 'error': str }
    """
    

    try:
        # Prepare temporary directory and zip file
        tmp_dir = tempfile.mkdtemp()
        filename = os.path.basename(sbml_path)
        zip_filename = os.path.splitext(filename)[0] + ".zip"
        zip_path = os.path.join(tmp_dir, zip_filename)

        # Create a zip file with the XML inside
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(sbml_path, arcname=filename)  # use arcname to avoid full path inside zip

        start_time = time.time()
        # Call SBMLKinetics
        df_classification, *_ = _dataSetStatistics(
            data_dir=tmp_dir,
            zip_filename=zip_filename,
            initial_model_indx=0,
            final_model_indx=1
        )

        elapsed = time.time() - start_time

        return {
            "time": elapsed,
            "classification": df_classification,
            "error": None
        }

    except Exception as e:
        return {
            "time": 0.0,
            "classification": None,
            "error": str(e)
        }

    finally:
        shutil.rmtree(tmp_dir)
