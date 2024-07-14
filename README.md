# Research Article Processing

This project involves searching for research articles manually, downloading their metadata, and using two Python scripts to gather and filter relevant articles.

## Steps to Process Articles

### 1. Manual Search and Metadata Download

Articles were searched for manually using various academic databases and journals. The metadata for these articles was then downloaded and saved in BibTeX format.

### 2. Filtering Relevant Articles

A Python script was used to filter the downloaded articles based on specific criteria such as peer-review status, recency, relevance, language, uniqueness, accessibility, and completeness. The filtered articles were then saved to a new BibTeX file.

### 3. Clustering and Further Filtering

Another Python script was used to process the filtered articles. This script involved:
- Extracting abstracts from the articles.
- Using TF-IDF vectorization to convert abstracts into numerical data.
- Clustering the articles based on their abstracts using KMeans clustering.
- Identifying relevant articles based on a specific keyword within the clusters.
- Saving the relevant articles to a final BibTeX file.

### Output

The output includes:
- A table displaying clusters with the top keywords for each cluster.
- A count of articles before and after filtering based on the specified keyword.
- The final set of relevant articles saved in a new BibTeX file.
