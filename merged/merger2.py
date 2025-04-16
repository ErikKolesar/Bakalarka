import json
import os

# Nastav cesty k priečinkom
SUMMARIES_DIR = "summaries"
FULL_ARTICLES_DIR = "full_articles"
OUTPUT_FILE = "merged_articles3.json"

summary_files = [f for f in os.listdir(SUMMARIES_DIR) if f.endswith(".json")]
full_files = [f for f in os.listdir(FULL_ARTICLES_DIR) if f.endswith(".json")]

# Tu sa budú ukladať sumáre, kľúčom je URL
summary_dict = {}

# ========== 1) Načítanie sumárov ==========

for sf in summary_files:
    path_summ = os.path.join(SUMMARIES_DIR, sf)
    with open(path_summ, "r", encoding="utf-8") as f:
        # Načítaj JSON
        data = json.load(f)

        # Ak je data dict, sprav z neho list
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            print(f"[UPOZORNENIE] Súbor {sf} neobsahuje list ani dict, preskakujem...")
            continue

        # Prejdi každý záznam v liste
        for article in data:
            if not isinstance(article, dict):
                print(f"[UPOZORNENIE] V súbore {sf} je položka, ktorá nie je dict: {article}")
                continue
            url = article.get("url")
            if url:
                summary_dict[url] = article

# ========== 2) Načítanie full článkov a spájanie so sumármi ==========

merged_list = []

for ff in full_files:
    path_full = os.path.join(FULL_ARTICLES_DIR, ff)
    with open(path_full, "r", encoding="utf-8") as f:
        data = json.load(f)

        # Ak je data dict, sprav z neho list
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            print(f"[UPOZORNENIE] Súbor {ff} neobsahuje list ani dict, preskakujem...")
            continue

        for full_article in data:
            if not isinstance(full_article, dict):
                print(f"[UPOZORNENIE] V súbore {ff} je položka, ktorá nie je dict: {full_article}")
                continue

            url = full_article.get("url")
            if url and url in summary_dict:
                # Vytvor kópiu sumáru
                merged_record = dict(summary_dict[url])
                # Pridaj full_content
                merged_record["full_content"] = full_article.get("full_content", "")
                merged_list.append(merged_record)

# ========== 3) Uloženie zlúčených záznamov ==========

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(merged_list, out, ensure_ascii=False, indent=2)

print(f"✅ Merged {len(merged_list)} articles into '{OUTPUT_FILE}'")
