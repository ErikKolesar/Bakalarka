import json
import os
import trafilatura

summary_folder = "summaries"
full_folder = "full_articles"

json_files = [
    "scraped_ai.json",
    "scraped_crypto.json",
    "scraped_design.json",
    "scraped_devops.json",
    "scraped_founders.json",
    "scraped_infosec.json",
    "scraped_marketing.json",
    "scraped_product.json",
    "scraped_tech.json",
    "scraped_webdev.json"
]

total_files = len(json_files)

for index, summary_file in enumerate(json_files, start=1):
    print(f"\n=== Processing {index}/{total_files}: {summary_file} ===")

    summary_path = os.path.join(summary_folder, summary_file)
    full_file = summary_file.replace(".json", "_full.json")
    full_path = os.path.join(full_folder, full_file)

    if not os.path.exists(summary_path):
        print(f"❌ Missing summary file: {summary_path}")
        continue

    # Load summaries
    with open(summary_path, "r", encoding="utf-8") as f:
        summaries = json.load(f)

    # Load or initialize full articles
    full_articles = []
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            try:
                full_articles = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON in {full_path}, starting fresh.")

    # Get the last URL in full_articles (if any)
    last_url = full_articles[-1]["url"] if full_articles else None

    # Find the index of last_url in summaries
    start_index = 0
    if last_url:
        for i, entry in enumerate(summaries):
            if entry.get("url") == last_url:
                start_index = i + 1  # Start from the next one
                break

    new_entries = []
    for entry in summaries[start_index:]:
        url = entry.get("url")
        if not url:
            continue

        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                extracted_data = trafilatura.extract(
                    downloaded,
                    output_format="json",
                    include_comments=False,
                    include_formatting=False,
                    target_language="en",
                    no_fallback=True,
                    with_metadata=True
                )
                if extracted_data:
                    extracted_json = json.loads(extracted_data)
                    article_text = extracted_json.get("text", "").strip()
                    metadata = extracted_json.get("metadata", {})

                    full_article = {
                        "title": entry.get("title"),
                        "url": url,
                        "category": entry.get("category"),
                        "full_content": article_text,
                        "metadata": metadata
                    }

                    new_entries.append(full_article)
                    print(f"✅ Added: {url}")
                else:
                    print(f"⚠️ No extractable content for: {url}")
            else:
                print(f"⚠️ Could not download: {url}")
        except Exception as e:
            print(f"⚠️ Error processing {url}: {e}")

    if new_entries:
        full_articles.extend(new_entries)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(full_articles, f, indent=4, ensure_ascii=False)
        print(f"💾 Updated {full_file} with {len(new_entries)} new articles. Total now: {len(full_articles)}")
    else:
        print(f"ℹ️ No new articles to add to {full_file}")
