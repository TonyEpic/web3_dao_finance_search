import os
os.environ['LOKY_MAX_CPU_COUNT'] = '1'

import bibtexparser
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
from tabulate import tabulate

nltk.download('punkt')
nltk.download('stopwords')

def load_bib_file(file_path):
    with open(file_path, encoding='utf-8') as bib_file:
        bib_database = bibtexparser.load(bib_file)
    return bib_database

def extract_abstracts(entries):
    abstracts = []
    for entry in entries:
        if 'abstract' in entry:
            abstracts.append(entry['abstract'])
    return abstracts

def extract_keywords(abstracts, max_features=1000):
    stop_words = list(nltk.corpus.stopwords.words('english'))
    vectorizer = TfidfVectorizer(max_features=max_features, stop_words=stop_words)
    X = vectorizer.fit_transform(abstracts)
    feature_names = vectorizer.get_feature_names_out()
    return feature_names, X

def cluster_keywords(X, num_clusters=10):
    # Dimensionality reduction for better clustering
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X.toarray())
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(X_reduced)
    return kmeans.labels_

def trace_articles_by_clusters(entries, labels, keyword, num_clusters):
    relevant_entries = []
    clusters = {i: [] for i in range(num_clusters)}
    
    for entry, label in zip(entries, labels):
        if 'abstract' in entry and keyword.lower() in entry['abstract'].lower():
            clusters[label].append(entry)
    
    for cluster in clusters.values():
        relevant_entries.extend(cluster)
    
    return relevant_entries

def save_bib_file(entries, file_path):
    bib_database = bibtexparser.bibdatabase.BibDatabase()
    bib_database.entries = entries
    with open(file_path, 'w', encoding='utf-8') as bib_file:
        bibtexparser.dump(bib_database, bib_file)

def display_clusters(clusters):
    cluster_table = []
    for label, keywords in clusters.items():
        cluster_table.append([label, ', '.join(set(keywords[:20]))])  # Limit to top 20 keywords per cluster
    df = pd.DataFrame(cluster_table, columns=['Cluster', 'Keywords'])
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def main(input_file, num_clusters, keyword):
    bib_database = load_bib_file(input_file)
    original_count = len(bib_database.entries)
    
    abstracts = extract_abstracts(bib_database.entries)
    keywords, X = extract_keywords(abstracts)
    labels = cluster_keywords(X, num_clusters)
    
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(keywords[i])
    display_clusters(clusters)
    
    relevant_entries = trace_articles_by_clusters(bib_database.entries, labels, keyword, num_clusters)
    filtered_count = len(relevant_entries)
    
    output_file = f"filtered_articles_{keyword.replace(' ', '_')}.bib"
    if filtered_count > 0:
        save_bib_file(relevant_entries, output_file)
    
    print(f"Number of articles before filtering: {original_count}")
    print(f"Number of articles after filtering: {filtered_count}")
    print(f"Filtered articles saved to {output_file}")

if __name__ == "__main__":
    input_file = "filtered_articles.bib"  # Replace with your .bib file path

    num_clusters = 10  
    keyword = "security and privacy"  # Input word for filtering
    main(input_file, num_clusters, keyword)
