import pandas as pd
import os

def validate_and_prep_ingestion(csv_path):
    if not os.path.exists(csv_path):
        print(f"[ERROR] Registry file not found at {csv_path}")
        return False
        
    df = pd.read_csv(csv_path)
    required_columns = ['date', 'sector', 'title', 'video_style', 'video_voiceover_prompt']
    
    # Verify internal schema integrity
    if not all(col in df.columns for col in required_columns):
        print("[ERROR] Internal OS Schema Mismatch. Aborting ingestion loop.")
        return False
        
    print(f"[SUCCESS] {len(df)} live vectors validated. Ready for notebook video pipeline sync.")
    return df

if __name__ == "__main__":
    validate_and_prep_ingestion("../../data/tenders/master_registry.csv")
