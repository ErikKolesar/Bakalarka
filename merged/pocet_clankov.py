import json

with open("merged_articles.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print("Number of articles:", len(data))



with open("cleaned_articles.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print("Number of articles:", len(data))

with open("missing_articles.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print("Number of articles:", len(data))