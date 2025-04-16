import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import hashlib

# JSON files stored in the 'summaries' folder
json_folder = "summaries"
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
    "scraped_webdev.json",
]

# Base URLs for each category
category_base_urls = {
    "tech": "https://tldr.tech/tech",
    "webdev": "https://tldr.tech/webdev",
    "ai": "https://tldr.tech/ai",
    "infosec": "https://tldr.tech/infosec",
    "product": "https://tldr.tech/product",
    "devops": "https://tldr.tech/devops",
    "founders": "https://tldr.tech/founders",
    "design": "https://tldr.tech/design",
    "marketing": "https://tldr.tech/marketing",
    "crypto": "https://tldr.tech/crypto",
}

def generate_unique_key(category, date, title):
    title_hash = hashlib.sha256(title.encode("utf-8")).hexdigest()
    return f"{category}_{date}_{title_hash[:8]}"

def get_last_date_from_json(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            articles = json.load(f)
            if not articles:
                return None
            dates = [datetime.strptime(article["date"], "%Y-%m-%d") for article in articles]
            return max(dates)
        except json.JSONDecodeError:
            print(f"Error reading {file_path}, skipping...")
            return None

def generate_urls(base_url, start_date, end_date):
    urls = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        urls.append((f"{base_url}/{date_str}", date_str))
        current_date += timedelta(days=1)
    return urls

def extract_sections(url, date, category):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        sections = soup.find_all("section")
        articles_data = []

        for section in sections:
            try:
                header_element = section.find("h3", class_="text-center font-bold")
                if not header_element:
                    continue
                header_text = header_element.get_text(strip=True)
                if header_text.lower() == "quick links":
                    continue

                articles = section.find_all("article", class_="mt-3")

                for article in articles:
                    try:
                        title_element = article.find("a", class_="font-bold")
                        if not title_element:
                            continue
                        article_title = title_element.get_text(strip=True)
                        if "sponsor" in article_title.lower():
                            continue

                        article_link = title_element["href"]
                        content_div = article.find("div", class_="newsletter-html")
                        if not content_div:
                            continue
                        article_content = content_div.get_text(strip=True)

                        unique_key = generate_unique_key(category, date, article_title)

                        articles_data.append({
                            "unique_key": unique_key,
                            "title": article_title,
                            "url": article_link,
                            "content": article_content,
                            "date": date,
                            "category": category,
                        })
                    except Exception:
                        pass
            except Exception:
                pass
        return articles_data
    except Exception:
        print(f"Failed to process URL: {url} for date: {date} and category: {category}")
        return []

def update_json_files():
    for file in json_files:
        file_path = os.path.join(json_folder, file)
        category = file.replace("scraped_", "").replace(".json", "")

        if category not in category_base_urls:
            print(f"Skipping unknown category: {category}")
            continue

        last_date = get_last_date_from_json(file_path)
        start_date = last_date + timedelta(days=1) if last_date else datetime(2023, 1, 1)
        end_date = datetime.now()

        if start_date > end_date:
            print(f"No updates needed for {category} (already up-to-date)")
            continue

        print(f"Updating {category} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

        base_url = category_base_urls[category]
        urls_with_dates = generate_urls(base_url, start_date, end_date)

        new_articles = []
        for url, date in urls_with_dates:
            new_articles.extend(extract_sections(url, date, category))

        if new_articles:
            existing_articles = []
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        existing_articles = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Warning: Unable to read {file_path}, overwriting with new data")

            updated_articles = existing_articles + new_articles

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(updated_articles, f, ensure_ascii=False, indent=4)

            print(f"Updated {file_path} with {len(new_articles)} new articles. Total: {len(updated_articles)}")
        else:
            print(f"No new articles found for {category}")

if __name__ == "__main__":
    update_json_files()
