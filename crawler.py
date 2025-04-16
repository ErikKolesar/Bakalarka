import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import hashlib

# Function to generate a unique key for each article
def generate_unique_key(category, date, title):
    # Use a hash function to create a unique identifier from the title
    title_hash = hashlib.sha256(title.encode('utf-8')).hexdigest()
    return f"{category}_{date}_{title_hash[:8]}"  # Shorten hash for brevity

# Function to extract all data from sections
def extract_sections(url, date, category):
    try:
        # print(f"Processing URL: {url} for date: {date} and category: {category}")

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <section> elements
        sections = soup.find_all('section')

        # List to store the extracted data
        articles_data = []

        for section in sections:
            try:
                # Extract the section's header
                header_element = section.find('h3', class_='text-center font-bold')
                if not header_element:
                    continue
                header_text = header_element.get_text(strip=True)

                # Skip sections named "Quick Links"
                if header_text.lower() == "quick links":
                    continue

                # Find all articles in the section
                articles = section.find_all('article', class_='mt-3')

                for article in articles:
                    try:
                        # Extract article URL and content
                        title_element = article.find('a', class_='font-bold')
                        if not title_element:
                            continue
                        article_title = title_element.get_text(strip=True)

                        # Skip articles with "Sponsor" in the title
                        if "sponsor" in article_title.lower():
                            continue

                        article_link = title_element['href']
                        content_div = article.find('div', class_='newsletter-html')
                        if not content_div:
                            continue
                        article_content = content_div.get_text(strip=True)

                        # Generate a unique key for this article
                        unique_key = generate_unique_key(category, date, article_title)

                        # Append the article with unique key
                        articles_data.append({
                            'unique_key': unique_key,
                            'title': article_title,
                            'url': article_link,
                            'content': article_content,
                            'date': date,
                            'category': category,
                        })
                    except Exception:
                        pass
            except Exception:
                pass

        return articles_data

    except Exception:
        print(f"Failed to process URL: {url} for date: {date} and category: {category}")
        return []  # Return empty list on error

# Function to generate URLs for a range of dates
def generate_urls(base_url, start_date, end_date):
    urls = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        urls.append((f"{base_url}/{date_str}", date_str))
        current_date += timedelta(days=1)
    return urls

# Categories and their specific start dates
category_start_dates = {
    "tech": datetime(2018, 10, 1),
    "webdev": datetime(2023, 1, 1),
    "ai": datetime(2023, 1, 1),
    "infosec": datetime(2023, 1, 1),
    "product": datetime(2023, 1, 1),
    "devops": datetime(2023, 1, 1),
    "founders": datetime(2023, 1, 1),
    "design": datetime(2023, 1, 1),
    "marketing": datetime(2023, 1, 10),
    "crypto": datetime(2020, 1, 1),
}

# End date is always today's date
end_date = datetime.now()

# List of categories
categories = list(category_start_dates.keys())

# Scrape each category and save to its own file
for category in categories:
    # Get the start date for this category
    start_date = category_start_dates[category]
    base_url = f"https://tldr.tech/{category}"  # Category-specific base URL
    urls_with_dates = generate_urls(base_url, start_date, end_date)

    # List to store all scraped data for this category
    all_articles = []

    for url, date in urls_with_dates:
        # Extract sections and append articles
        articles = extract_sections(url, date, category)
        all_articles.extend(articles)

    # Save data to a JSON file for this category
    output_file = f"scraped_{category}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print(f"Scraping for category '{category}' complete. Data saved to {output_file}. Total articles: {len(all_articles)}")
