import os
import time
import pandas as pd
from ratesb_python import Analyzer
from sbmlk_wrapper import run_sbmlk_on_file

# Define benchmark directory
MODEL_DIR = "models"
XML = ".xml"

# Classification mappings between tools
SBMLK_TO_RATESB = {
    "UNDR": "UNDR1",  # SBMLKinetics doesn't distinguish UNDR1/UNDR2
    "MM": "MM",
    "FR": "GENERIC",  # FR is too generic - treat as wrong
    "BIDR": "BIDR21",  # SBMLKinetics doesn't distinguish BIDR subtypes
}

# Expected classifications for each model (ground truth in RatesB format)
EXPECTED_CLASSIFICATIONS = {
    "bidirectional_bidr21.xml": {"J0": "BIDR21"},
    "bidirectional_bidr_a11.xml": {"J0": "BIDR11"},
    "mass_action_undr1.xml": {"J0": "UNDR1"},
    "mass_action_undr2.xml": {"J0": "UNDR2"},
    "michaelis_menten_mm.xml": {"J0": "MM"},
    "michaelis_menten_mmcat.xml": {"J0": "MM"},
    "reversible_mm_rmm.xml": {"J0": "RMM"},
    "reversible_mm_rmmcat.xml": {"_J0": "RMMcat"},
    # New complex models
    "mixed_pathway_1.xml": {"J0": "UNDR1", "J1": "MM", "J2": "BIDR21"},
    "enzyme_cascade.xml": {"J0": "MMcat", "J1": "MMcat", "J2": "MMcat"},
    "branched_network.xml": {"J0": "UNDR1", "J1": "UNDR1", "J2": "BIDR21", "J3": "MM", "J4": "BIDR21"},
    "reversible_pathway.xml": {"J0": "BIDR11", "J1": "BIDR21", "J2": "BIDR12", "J3": "BIDR22"},
    "metabolic_cycle.xml": {"J0": "UNDR2", "J1": "MMcat", "J2": "RMM", "J3": "UNDR2", "J4": "BIDR11"}
}

def time_it(fn, *args, **kwargs):
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    end = time.perf_counter()
    return result, end - start

def get_ratesb_classifications(analyzer):
    """Extract classifications from ratesb_python analyzer"""
    classifications = {}
    for reaction_id, class_dict in analyzer.data.default_classifications.items():
        for classification, is_true in class_dict.items():
            if is_true:
                classifications[reaction_id] = classification
                break
        if reaction_id not in classifications:
            classifications[reaction_id] = "UNDF"
    return classifications

def get_sbmlk_classifications(sbmlk_output):
    """Extract classifications from SBMLKinetics output"""
    classifications = {}
    if sbmlk_output["error"] or sbmlk_output["classification"] is None:
        return classifications
    
    df = sbmlk_output["classification"]
    if not df.empty:
        for _, row in df.iterrows():
            reaction_id = row.get("Reaction id", "Unknown")  # Fixed column name
            classification = row.get("Classifications", "Unclassified")
            if pd.notna(classification) and classification:
                # Map SBMLKinetics classification to RatesB equivalent
                mapped_class = SBMLK_TO_RATESB.get(classification, classification)
                classifications[reaction_id] = mapped_class
            else:
                classifications[reaction_id] = "Unclassified"
    return classifications

def calculate_accuracy(expected, actual):
    """Calculate accuracy for a single model"""
    if not expected:
        return 0.0
    
    correct = 0
    total = len(expected)
    
    for reaction_id, expected_class in expected.items():
        actual_class = actual.get(reaction_id, "UNDF")
        
        if actual_class == expected_class:
            correct += 1
        elif actual_class == "GENERIC":  # FR and other generic classifications are wrong
            correct += 0  # No credit for generic classifications
        elif actual_class in ["UNDR1", "UNDR2"] and expected_class in ["UNDR1", "UNDR2"]:
            correct += 0.5  # Partial credit for UNDR type but wrong subtype
        elif actual_class.startswith("BIDR") and expected_class.startswith("BIDR"):
            correct += 0.5  # Partial credit for BIDR type but wrong subtype
    
    return correct / total

# Collect all SBML models
model_files = [f for f in os.listdir(MODEL_DIR) if f.endswith(XML)]
model_files.sort()

print(f"{'Model':<25} {'Reactions':<10} {'RatesB Acc':<12} {'SBMLK Acc':<12} {'RatesB Time':<12} {'SBMLK Time':<12}")
print("-" * 85)

total_ratesb_correct = 0
total_sbmlk_correct = 0
total_reactions = 0
total_ratesb_time = 0
total_sbmlk_time = 0

for filename in model_files:
    if filename not in EXPECTED_CLASSIFICATIONS:
        continue
        
    path = os.path.join(MODEL_DIR, filename)
    expected = EXPECTED_CLASSIFICATIONS[filename]
    num_reactions = len(expected)
    total_reactions += num_reactions

    # === ratesb_python ===
    ratesb_analyzer = Analyzer(path)
    _, ratesb_time = time_it(ratesb_analyzer.check_all)
    ratesb_classifications = get_ratesb_classifications(ratesb_analyzer)
    ratesb_accuracy = calculate_accuracy(expected, ratesb_classifications)
    
    total_ratesb_time += ratesb_time
    total_ratesb_correct += ratesb_accuracy * num_reactions

    # === SBMLKinetics ===
    sbmlk_output = run_sbmlk_on_file(path)
    sbmlk_time = sbmlk_output["time"]
    sbmlk_classifications = get_sbmlk_classifications(sbmlk_output)
    sbmlk_accuracy = calculate_accuracy(expected, sbmlk_classifications)
    
    total_sbmlk_time += sbmlk_time
    total_sbmlk_correct += sbmlk_accuracy * num_reactions

    # === OUTPUT ===
    print(f"{filename:<25} {num_reactions:<10} {ratesb_accuracy:<12.2%} {sbmlk_accuracy:<12.2%} {ratesb_time:<12.3f} {sbmlk_time:<12.3f}")

# Summary
print("-" * 85)
overall_ratesb_accuracy = total_ratesb_correct / total_reactions if total_reactions > 0 else 0
overall_sbmlk_accuracy = total_sbmlk_correct / total_reactions if total_reactions > 0 else 0

print(f"{'OVERALL':<25} {total_reactions:<10} {overall_ratesb_accuracy:<12.2%} {overall_sbmlk_accuracy:<12.2%} {total_ratesb_time:<12.3f} {total_sbmlk_time:<12.3f}")
print(f"\nStability Advantage: RatesB is {(overall_ratesb_accuracy - overall_sbmlk_accuracy)*100:.1f}% more accurate")