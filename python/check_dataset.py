
import pandas as pd
import os

# ==========================================
# STEP 1: LOAD DATASET
# ==========================================

file_path = "data/raw/economic_data.csv"

print("\n========== DATASET DIAGNOSTICS ==========")

# Check whether file exists
print("\n1. FILE CHECK:")
print("File exists:", os.path.exists(file_path))

if not os.path.exists(file_path):
    print("ERROR: Dataset file not found!")
    raise SystemExit

# Check file size
print("File size:", os.path.getsize(file