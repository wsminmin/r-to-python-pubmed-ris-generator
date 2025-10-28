# -----------------------------------------------------------------------------
# Objective:
#   Take a list of DOIs, retrieve metadata from PubMed, and export results
#   in RIS format (importable into EndNote).
#
# Notes:
#   1. Not all DOIs are found in PubMed.
#   2. After importing RIS into EndNote, right-click references and select
#      "Find Reference Updates" to complete details.
#   3. DO NOT scrape Google Scholar for missing DOIs — Google may block your IP.
# -----------------------------------------------------------------------------

# How to prepare a list of DOIs:
#   1. Open your Excel file and filter all articles for full-text screening.
#   2. Copy filtered DOIs into a new Excel workbook and save as both .xls and .txt.
#   3. Use the .txt file as input for this Python script.

# -----------------------------------------------------------------------------
# USER INPUT – Update these two paths before running
# -----------------------------------------------------------------------------
input_file  = r"DOIs testing set.txt"
output_file = r"pubmed_articles.ris"

# -----------------------------------------------------------------------------
# Setup environment
# -----------------------------------------------------------------------------
from Bio import Entrez
import pandas as pd
import re
import time

# Always tell NCBI who you are
Entrez.email = "minmin.tan@gmail.com"  # <-- replace with your real email

# -----------------------------------------------------------------------------
# Read and clean DOI list
# -----------------------------------------------------------------------------
data = pd.read_csv(input_file, sep="\t", dtype=str)
data.columns = [col.strip() for col in data.columns]  # clean column names
dois = data['DOI'].str.replace(r"^https?://(dx\.)?doi\.org/", "", regex=True).tolist()

print(f"Number of DOIs read: {len(dois)}")

# -----------------------------------------------------------------------------
# Function: Fetch metadata from PubMed and convert to RIS format
# -----------------------------------------------------------------------------
def fetch_pubmed_metadata_ris(doi):
    """Fetch metadata for a given DOI and return an RIS entry string."""
    query = f"{doi}[DOI]"
    try:
        search_result = Entrez.read(Entrez.esearch(db="pubmed", term=query))
        if not search_result["IdList"]:
            return None

        pubmed_id = search_result["IdList"][0]
        summary = Entrez.read(Entrez.esummary(db="pubmed", id=pubmed_id))[0]

        ris_entry = "\n".join([
            "TY  - JOUR",
            f"TI  - {summary.get('Title', '')}",
            f"JO  - {summary.get('FullJournalName', '')}",
            f"VL  - {summary.get('Volume', '')}",
            f"SP  - {summary.get('Pages', '')}",
            f"PY  - {summary.get('PubDate', '')[:4]}",
            f"DO  - {doi}",
            "ER  - ",
        ])
        return ris_entry
    except Exception as e:
        print(f"Error fetching DOI {doi}: {e}")
        return None

# -----------------------------------------------------------------------------
# Fetch all metadata, write RIS file, and track missing DOIs
# -----------------------------------------------------------------------------
not_found = []
with open(output_file, "w", encoding="utf-8") as out:
    for i, doi in enumerate(dois, start=1):
        print(f"Processing {i} of {len(dois)}: {doi}")
        ris_entry = fetch_pubmed_metadata_ris(doi)

        if ris_entry:
            out.write(ris_entry + "\n\n")
        else:
            print(f"No metadata found for DOI: {doi}")
            not_found.append(doi)

        time.sleep(0.3)  # be nice to NCBI servers

# -----------------------------------------------------------------------------
# Save list of missing DOIs (if any)
# -----------------------------------------------------------------------------
if not_found:
    missing_file = re.sub(r"\.ris$", "_not_found.txt", output_file)
    with open(missing_file, "w", encoding="utf-8") as f:
        f.write("Missing_DOIs\n")
        for doi in not_found:
            f.write(f"{doi}\n")
    print(f"Some DOIs were not found. Saved list to: {missing_file}")
else:
    print("All DOIs were found in PubMed.")

print(f"RIS file created successfully: {output_file}")
