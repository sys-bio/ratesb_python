import os
import time
from ratesb_python import Analyzer
from sbmlk_wrapper import run_sbmlk_on_file

# Define benchmark directory
MODEL_DIR = "models"
XML = ".xml"

# Helper for timing
def time_it(fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    end = time.perf_counter()
    return result, end - start

# Collect all SBML models in the directory
model_files = [f for f in os.listdir(MODEL_DIR) if f.endswith(XML)]
model_files.sort()

print(f"{'Model':<25} {'RatesB Time (s)':<15} {'SBMLK Time (s)':<15} {'RatesB Class':<20} {'SBMLK Class':<20}")

for filename in model_files:
    path = os.path.join(MODEL_DIR, filename)

    # === ratesb_python ===
    ratesb_analyzer = Analyzer(path)
    _, ratesb_time = time_it(ratesb_analyzer.check_all)

    ratesb_result = ratesb_analyzer.results
    ratesb_class = ratesb_analyzer.data.default_classifications
    # default classifications is a dict with keys as reaction IDs, and values as a dict with keys Classification, and values True or False
    # only find the true classification (there should be only one or less), else UNDF
    ratesb_type_summary = "UNDF"
    for reaction_id, classifications in ratesb_class.items():
        for classification, is_true in classifications.items():
            if is_true:
                ratesb_type_summary = classification
                break

    # === SBMLKinetics ===
    sbml_path = os.path.join(MODEL_DIR, filename)  # assumes filename is .xml
    sbmlk_output = run_sbmlk_on_file(sbml_path)
    sbmlk_time = sbmlk_output["time"]

    if sbmlk_output["error"]:
        sbmlk_type_summary = "Error"
    else:
        df = sbmlk_output["classification"]
        if not df.empty:
            sbmlk_type_summary = ", ".join(df["Classifications"].dropna().unique())
        else:
            sbmlk_type_summary = "Unclassified"

    # === OUTPUT ===
    print(f"{filename:<25} {ratesb_time:<15.5f} {sbmlk_time:<15.5f} {ratesb_type_summary:<20} {sbmlk_type_summary:<20}")
