import argparse
import pandas as pd
import json

def convert_excel_to_json(excel_path, json_path):
    elo_data = pd.read_excel(excel_path, header=None)

    cleaned_data = {}
    for i in range(0, elo_data.shape[1], 2):
        player_names = elo_data.iloc[:, i].dropna()
        player_ratings = elo_data.iloc[:, i + 1].dropna()
        for name, rating in zip(player_names, player_ratings):
            cleaned_data[name] = rating

    json_data = json.dumps(cleaned_data, ensure_ascii=False, indent=4)
    
    with open(json_path, 'w', encoding='utf-8') as file:
        file.write(json_data)
    print(f"File converted successfully and saved as {json_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Excel to JSON for Go player ratings')
    parser.add_argument('--excel_path', type=str, required=True, help='Path to the Excel file containing ELO ratings')
    parser.add_argument('--json_path', type=str, required=True, help='Output path for the JSON file')

    args = parser.parse_args()
    convert_excel_to_json(args.excel_path, args.json_path)
