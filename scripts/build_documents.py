import json
from pathlib import Path

CATALOG_PATH = "data/shl_product_catalog.json"

with open(CATALOG_PATH, "r", encoding= "utf-8") as f:
    catalog = json.load(f)

documents = []
metadata = []

for assessment in catalog:

    name = assessment.get("name", "")
    description = assessment.get("description", "")

    job_levels = ", ".join(
        assessment.get("job_levels", [])
    )

    categories = ", ".join(
        assessment.get("keys", [])
    )

    languages = ", ".join(
        assessment.get("languages", [])
    )

    duration = assessment.get("duration", "")

    document = f"""
Name: {name}

Description:
{description}

Categories:
{categories}

Languages:
{languages}

Duration:
{duration}
""".strip()
    documents.append(document)
    metadata.append(
         {
            "name": name,
            "url": assessment.get("link", ""),
            "duration": duration,
            "languages": assessment.get("languages", []),
            "job_levels": assessment.get("job_levels", []),
            "categories": assessment.get("keys", [])
        }
    )
Path("data").mkdir(exist_ok=True) 
with open(
    "data/documents.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        documents,
        f,
        ensure_ascii=False,
        indent=2
    )

with open(
    "data/metadata.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        metadata,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"Built {len(documents)} documents")
print("Saved:")
print("- data/documents.json")
print("- data/metadata.json")


import json

with open("data/documents.json","r",encoding="utf-8") as f:
    docs = json.load(f)

print(docs[0])