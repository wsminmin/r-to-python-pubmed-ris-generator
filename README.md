# 🧬 r-to-python-pubmed-ris-generator

### Retrieve PubMed metadata from DOIs and export RIS files (R & Python versions)

---

## 📘 Overview

This repository contains **R** and **Python** scripts to take a list of **DOIs (Digital Object Identifiers)**, retrieve corresponding **metadata from PubMed**, and export the results in **RIS format**, ready for import into **EndNote** or other reference managers.

The project demonstrates how the same workflow can be implemented in both R and Python for automated literature metadata retrieval.

---

## 🎯 Objectives

- Read a list of DOIs from a `.txt` file  
- Query PubMed via the **NCBI Entrez API**  
- Retrieve key metadata (title, journal, volume, pages, publication year)  
- Export results into **RIS format**  
- Save a list of **DOIs not found** in PubMed  

---

## 📁 Repository Structure
```
r-to-python-pubmed-ris-generator/
│
├── R/
│ └── pubmed_ris_generator.R
│
├── Python/
│ └── pubmed_ris_generator.py
│
├── DOIs testing set.txt
├── pubmed_articles.ris
├── pubmed_articles_not_found.txt
└── README.md
```

---

## ⚙️ Setup

### 1️⃣ Clone this repository

```bash
git clone https://github.com/<your-username>/r-to-python-pubmed-ris-generator.git
cd r-to-python-pubmed-ris-generator
```
2️⃣ Install Python dependencies

Open a terminal and run:
```
pip install -r requirements.txt
```
For R, install the required package:
```
install.packages("rentrez")
```
**📂 Input File Format**

Prepare a tab-separated text file (.txt) with a column named DOI.

Example (DOIs testing set.txt):
```
https://dx.doi.org/10.1101/2022.09.06.22279606
https://dx.doi.org/10.1101/2022.09.02.22279519
https://dx.doi.org/10.1101/2022.03.03.22271672
https://dx.doi.org/10.1016/S1473-3099%2823%2900200-1
https://dx.doi.org/10.1001/jamanetworkopen.2021.47363
https://dx.doi.org/10.1016/j.ijid.2021.07.005
https://dx.doi.org/10.1016/j.genrep.2021.101267
https://dx.doi.org/10.1016/S2214-109X%2823%2900189-4
https://dx.doi.org/10.1097/INF.0000000000002761
https://dx.doi.org/10.3390/diagnostics12061505
```
**🧾 Output Files**

1. **RIS file** – formatted bibliographic data ready for EndNote
Example: pubmed_articles.ris
2. **Missing DOI list** – DOIs not found in PubMed
Example: pubmed_articles_not_found.txt

**⚠️ Notes**

- Not all DOIs exist in PubMed (e.g., preprints, non-biomedical papers).
- Do not scrape Google Scholar — it violates their terms and may block your IP.
- Use this script responsibly for research and educational purposes.

### 🔍 Why I made this
I created this project to:
- Streamline the process of collecting metadata from PubMed for multiple DOIs.  
- Provide both **R and Python implementations** so researchers can choose their preferred language.  
- Automate the creation of **RIS files**, saving time when managing references in EndNote.  

