import pandas as pd
import re
import json

# 1) Načítanie dát
df = pd.read_json("merged_articles.json")

# 2) Zjednotenie kategórií
df["category"] = df["category"].str.lower()

# 3) Čistenie textov
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["content"] = df["content"].apply(clean_text)
df["full_content"] = df["full_content"].apply(clean_text)

# 4) Definícia masiek
#    a) sociálne URL (twitter, x.com, linkedin)
social_mask = df["url"].str.contains("twitter.com|x.com|linkedin.com", na=False)

#    b) chýbajúci obsah
missing_mask = (df["content"] == "") | (df["full_content"] == "")

#    c) duplicity
duplicate_mask = df.duplicated(subset=["unique_key", "url"], keep=False)

# 5) Kombinovaná maska pre "problematické" záznamy (missing/duplicate/social)
to_remove_mask = social_mask | missing_mask | duplicate_mask

# 6) Rozdelenie na missing_content_df a clean_df
missing_content_df = df[to_remove_mask].copy()
clean_df = df[~to_remove_mask].copy()

# 7) Prevod dátumu na reťazec (YYYY-MM-DD)
clean_df["date"] = pd.to_datetime(clean_df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
missing_content_df["date"] = pd.to_datetime(missing_content_df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

# 8) Uloženie do JSON (tentoraz mená súborov zladíme s tvojím testovacím kódom)
with open("cleaned_articles.json", "w", encoding="utf-8") as f:
    json.dump(clean_df.to_dict(orient="records"), f, indent=2, ensure_ascii=False)

with open("missing_articles.json", "w", encoding="utf-8") as f:
    json.dump(missing_content_df.to_dict(orient="records"), f, indent=2, ensure_ascii=False)

# 9) Náhrada \/ späť na /
def unescape_slashes(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("\\/", "/")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

unescape_slashes("cleaned_articles.json")
unescape_slashes("missing_articles.json")

# 10) (Nepovinné) Výpis kontrolného súčtu
print(f"Vstupný súbor (merged_articles.json): {len(df)} článkov")
print(f"Missing/dup/social: {len(missing_content_df)}")
print(f"Clean:              {len(clean_df)}")
print(f"Súčet:              {len(missing_content_df) + len(clean_df)}")
