from pathlib import Path
import sys

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    print("Missing dependency: pypdf")
    print("Install it with: pip install pypdf")
    sys.exit(1)


# Common locations depending on where this is run.
candidate_paths = [
    Path(r"C:\Users\Kade\Downloads\README.pdf"),
    Path("README.pdf"),
    Path("/workspaces/qm2023-capstone-arjun-daemian-kade-isidro/README.pdf"),
]

pdf_path = next((p for p in candidate_paths if p.exists()), None)
if pdf_path is None:
    print("Could not find README.pdf.")
    print("Place README.pdf in this project folder or update candidate_paths.")
    print("Checked:")
    for p in candidate_paths:
        print(f" - {p}")
    sys.exit(1)

reader = PdfReader(str(pdf_path))
print(f"Reading: {pdf_path}")
print(f"Pages: {len(reader.pages)}")

all_text = []
for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    all_text.append(f"\n--- Page {i} ---\n{text}")

full_text = "\n".join(all_text)
print(full_text[:1000])

output_txt = pdf_path.with_suffix(".txt")
output_txt.write_text(full_text, encoding="utf-8")
print(f"Saved extracted text to: {output_txt}")
