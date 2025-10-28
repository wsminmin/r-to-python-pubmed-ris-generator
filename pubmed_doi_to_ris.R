# -------------------------------------------------------------------------
# Objective:
#   Take a list of DOIs, retrieve metadata from PubMed, and export results
#   in RIS format (importable into EndNote).
#
# Notes:
#   1. Not all DOIs are found in PubMed.
#   2. After importing RIS into EndNote, right-click references and select
#      "Find Reference Updates" to complete details.
#   3. DO NOT scrape Google Scholar for missing DOIs — Google may block your IP.
# -------------------------------------------------------------------------

# How to prepare a list of DOIs:
#   1. Open the Excel file at the provided SharePoint link.
#   2. In 'Screening_Obj1' sheet, filter all articles included for full text screening.
#   3. Copy filtered DOIs into a new Excel workbook and save as both .xls and .txt.
#   4. Use the .txt file as input for this R script.

# -------------------------------------------------------------------------
# USER INPUT – Update these two paths before running
# -------------------------------------------------------------------------
rm(list = ls())

input_file  <- "DOIs testing set.txt"
output_file <- "pubmed_articles.ris"


# -------------------------------------------------------------------------
# Setup environment
# -------------------------------------------------------------------------
if (!require("rentrez", quietly = TRUE)) {
  install.packages("rentrez", dependencies = TRUE)
  library(rentrez)
}

# -------------------------------------------------------------------------
# Read and clean DOI list
# -------------------------------------------------------------------------
data <- read.table(input_file, header = TRUE, sep = "\t", quote = "", stringsAsFactors = FALSE)
dois <- gsub("^https?://(dx\\.)?doi\\.org/", "", data$DOI)

cat("Number of DOIs read:", length(dois), "\n")

# -------------------------------------------------------------------------
# Function: Fetch metadata from PubMed and convert to RIS format
# -------------------------------------------------------------------------
fetch_pubmed_metadata_ris <- function(doi) {
  query <- paste0(doi, "[DOI]")
  search_result <- entrez_search(db = "pubmed", term = query)
  if (is.null(search_result$count) || search_result$count == 0) return(NULL)
  
  id <- search_result$ids[1]  # take first result
  summary <- entrez_summary(db = "pubmed", id = id)
  
  ris_entry <- paste(
    "TY  - JOUR",
    paste0("TI  - ", summary$title),
    paste0("JO  - ", summary$source),
    paste0("VL  - ", summary$volume),
    paste0("SP  - ", summary$pages),
    paste0("PY  - ", substr(summary$pubdate, 1, 4)),
    paste0("DO  - ", doi),
    "ER  - ",
    sep = "\n"
  )
  return(ris_entry)
}

# -------------------------------------------------------------------------
# Fetch all metadata, write RIS file, and track missing DOIs
# -------------------------------------------------------------------------
not_found <- c()
con <- file(output_file, "w")

for (i in seq_along(dois)) {
  doi <- dois[i]
  cat("Processing", i, "of", length(dois), ":", doi, "\n")
  ris_entry <- fetch_pubmed_metadata_ris(doi)
  
  if (!is.null(ris_entry)) {
    cat(ris_entry, "\n\n", file = con)
  } else {
    cat("No metadata found for DOI:", doi, "\n")
    not_found <- c(not_found, doi)
  }
}

close(con)

# -------------------------------------------------------------------------
# Save list of missing DOIs (if any)
# -------------------------------------------------------------------------
if (length(not_found) > 0) {
  missing_file <- gsub("\\.ris$", "_not_found.txt", output_file)
  write.table(not_found, file = missing_file, quote = FALSE, row.names = FALSE, col.names = "Missing_DOIs")
  cat("Some DOIs were not found. Saved list to:", missing_file, "\n")
} else {
  cat("All DOIs were found in PubMed.\n")
}

cat("RIS file created successfully:", output_file, "\n")

# -------------------------------------------------------------------------
# End of script
# -------------------------------------------------------------------------
