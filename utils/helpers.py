import json
from pathlib import Path
from datetime import datetime
import random

def save_json(data):
    # Generate filename
    filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000,9999)}.json"    
    filepath = Path(__file__).parent.parent / 'results' / filename

    # Write file
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
