import pandas as pd
from fastapi import HTTPException
import os
from pathlib import Path

def load_data():

    try:

        project_root = Path(__file__).parent
        csv_path = project_root / "datafeed.csv"
        
        if not csv_path.exists():

            raise (FileNotFoundError(f"File not found: {csv_path}"))
        #
            
        df = pd.read_csv(csv_path)
        return (df)
    #
    except Exception as e:

        raise (HTTPException(status_code=500, detail=f"Error loading data: {str(e)}"))
    #
#

last_timestamp = load_data()['timestamp'].max() // 1000
