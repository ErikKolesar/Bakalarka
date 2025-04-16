import json

# List of JSON filenames
json_files = [
    "scraped_ai_full.json",
    "scraped_crypto_full.json",
    "scraped_design_full.json",
    "scraped_devops_full.json",
    "scraped_founders_full.json",
    "scraped_infosec_full.json",
    "scraped_marketing_full.json",
    "scraped_product_full.json",
    "scraped_tech_full.json",
    "scraped_webdev_full.json",
]

total_count = 0 

for filename in json_files:
    with open("full_articles/" + filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        count = len(data)
        print(f"{filename}: {count}")
        total_count += count


print(f"\nTotal number of JSON objects across all files: {total_count}")


# import json
# import os

# # List of JSON filenames in the summaries folder
# json_files = [
#     "scraped_ai.json",
#     "scraped_crypto.json",
#     "scraped_design.json",
#     "scraped_devops.json",
#     "scraped_founders.json",
#     "scraped_infosec.json",
#     "scraped_marketing.json",
#     "scraped_product.json",
#     "scraped_tech.json",
#     "scraped_webdev.json",
# ]

# total_count = 0
# folder = "summaries"

# for filename in json_files:
#     file_path = os.path.join(folder, filename)
#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         count = len(data)
#         print(f"{filename}: {count}")
#         total_count += count

# print(f"\nTotal number of JSON objects across all files: {total_count}")



