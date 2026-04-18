import pandas as pd
from pathlib import Path

def get_output_path(default_dir: str, custom_path: str):
    """Determines the correct directory path."""
    if custom_path:
        return Path(custom_path)
    else:
        # Uses the current working directory if default is chosen
        return Path.cwd() 

def save_to_sheet(output_dir: Path, new_data: dict):
    """Handles creating or editing the Excel sheet."""
    file_name = "job_tracking_sheet.xlsx"
    full_path = output_dir / file_name
    
    # Create a DataFrame from the single new record
    new_row_df = pd.DataFrame([new_data])
    
    if full_path.exists():
        print(f"✅ File found. Appending data to: {full_path}")
        # Read existing data, append new row, and overwrite
        try:
            existing_df = pd.read_excel(full_path)
            updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)
            updated_df.to_excel(full_path, index=False)
        except Exception as e:
            print(f"Error reading existing file: {e}. Starting fresh.")
            new_row_df.to_excel(full_path, index=False) # Fallback to overwrite if read fails
    else:
        print(f"✅ Creating new tracking sheet at: {full_path}")
        new_row_df.to_excel(full_path, index=False)

