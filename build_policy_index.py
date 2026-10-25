import json
from pathlib import Path
from urllib.parse import quote
import fitz

ROOT = Path("policies")
OUTPUT = Path("policy_index.json")

REPO = "ICU-NURSING-ASSISSTANT-AI/icu-smart-hup"
BRANCH = "main"

records = []
files_count = 0

for pdf in sorted(ROOT.rglob("*.pdf")):
    files_count += 1
    relative_path = pdf.relative_to(ROOT)
    parts = relative_path.parts

    unit = parts[0] if len(parts) > 1 else "General"
    hospital = parts[1] if len(parts) > 2 else "General"

    url = (
        f"https://github.com/{REPO}/blob/{BRANCH}/"
        + quote(pdf.as_posix(), safe="/")
    )

    try:
        with fitz.open(pdf) as document:
           for page_number, page in enumerate(document, 1):
              text = page.get_text("text", sort=False).strip()

                if not text:
                    continue

                records.append({
                    "unit": unit,
                    "hospital": hospital,
                    "policy": pdf.name,
                    "page": page_number,
                    "text": text,
                    "url": url
                })

    except Exception as error:
        print(f"Error reading {pdf}: {error}")

OUTPUT.write_text(
    json.dumps(records, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"PDF files found: {files_count}")
print(f"Indexed pages: {len(records)}")
print(f"Index saved to: {OUTPUT}")
