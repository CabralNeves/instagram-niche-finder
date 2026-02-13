import pandas as pd
import json
import os
from datetime import datetime

def save_to_json(data, filename):
    filepath = os.path.join("data", f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filepath}")
    return filepath

def save_to_csv(data, filename):
    filepath = os.path.join("data", f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"Data saved to {filepath}")
    return filepath
