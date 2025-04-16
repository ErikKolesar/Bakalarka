# import json
# import random

# # Paths to JSON files
# output_path = "merged/merged_articles.json"
# random_output_path = "merged/random_100_articles.json"

# # Load merged articles
# with open(output_path, "r", encoding="utf-8") as f:
#     merged_articles = json.load(f)

# # Print total number of merged articles
# print(f"Total merged articles: {len(merged_articles)}")

# # Select 100 random articles
# random_articles = random.sample(merged_articles, min(100, len(merged_articles)))

# # Save random articles
# with open(random_output_path, "w", encoding="utf-8") as f:
#     json.dump(random_articles, f, indent=4, ensure_ascii=False)

# print(f"Random 100 articles saved to {random_output_path}")


import json

# Replace with your JSON file path
JSON_FILE = "missing_articles.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

count_twitter = 0
count_xcom = 0
count_linkedin = 0

for item in data:
    # Safely get the URL string; if missing, default to empty
    url = item.get("url", "")
    
    # Check for partial string matches
    if "twitter.com" in url:
        count_twitter += 1
    if "x.com" in url:
        count_xcom += 1
    if "linkedin.com" in url:
        count_linkedin += 1

print("Occurrences of Twitter URLs:", count_twitter)
print("Occurrences of X.com URLs:", count_xcom)
print("Occurrences of LinkedIn URLs:", count_linkedin)
