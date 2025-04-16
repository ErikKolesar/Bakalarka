import os
import json
import re

# Directory containing your JSON files
data_dir = "."

# Get all files in the directory
files = os.listdir(data_dir)

# Filter to find only the *_cleaned.json files
cleaned_files = [f for f in files if f.endswith("_cleaned.json")]

for cleaned_file in cleaned_files:
    # Build the path to the cleaned file
    cleaned_path = os.path.join(data_dir, cleaned_file)

    # Infer the corresponding main file by removing "_cleaned"
    main_file = cleaned_file.replace("_cleaned", "")
    main_path = os.path.join(data_dir, main_file)

    # Decide on an output file name, e.g. scraped_ai_merged.json
    # or overwrite the original. Here, let's create a merged file:
    merged_file = main_file.replace(".json", "_merged.json")
    merged_path = os.path.join(data_dir, merged_file)

    # If the main file doesn’t exist, skip
    if not os.path.exists(main_path):
        print(f"WARNING: Main file not found for {cleaned_file}")
        continue

    print(f"Merging {main_file} with {cleaned_file}")

    # Load the data
    with open(main_path, "r", encoding="utf-8") as f:
        main_data = json.load(f)

    with open(cleaned_path, "r", encoding="utf-8") as f:
        cleaned_data = json.load(f)

    # Build a dictionary keyed by URL
    cleaned_dict = {}
    for entry in cleaned_data:
        url = entry["url"]
        cleaned_dict[url] = entry

    # Merge into the main_data
    for item in main_data:
        url = item["url"]
        if url in cleaned_dict:
            item["full_content"] = cleaned_dict[url].get("full_content")

    # Write out the merged file
    with open(merged_path, "w", encoding="utf-8") as f:
        json.dump(main_data, f, indent=4, ensure_ascii=False)

    print(f" -> Created {merged_file}\n")
