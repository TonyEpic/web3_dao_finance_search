import os
import bibtexparser
from datetime import datetime

def load_bib_file(file_path):
    with open(file_path, encoding='utf-8') as bib_file:
        bib_database = bibtexparser.load(bib_file)
    return bib_database

def save_bib_file(bib_database, output_path):
    with open(output_path, 'w', encoding='utf-8') as bib_file:
        bibtexparser.dump(bib_database, bib_file)

def is_peer_reviewed(entry):
    return entry['ENTRYTYPE'] in ['article', 'inproceedings', 'conference']

def is_recent(entry):
    current_year = datetime.now().year
    return 'year' in entry and current_year - int(entry['year']) <= 10

def is_relevant(entry):
    keywords = ['web3', 'dao', 'blockchain', 'decentralized']
    return any(keyword.lower() in entry.get('title', '').lower() for keyword in keywords)

def is_english(entry):
    return 'language' not in entry or entry['language'].lower() == 'english'

def is_not_duplicate(entry, seen_titles):
    title = entry.get('title', '').lower()
    if title in seen_titles:
        return False
    seen_titles.add(title)
    return True

def is_accessible(entry):
    return 'url' in entry or 'doi' in entry

def is_complete(entry):
    return entry['ENTRYTYPE'] not in ['abstract', 'preliminary']

def filter_entries(entries):
    filtered_entries = []
    seen_titles = set()
    
    for entry in entries:
        if (is_peer_reviewed(entry) and
            is_recent(entry) and
            is_relevant(entry) and
            is_english(entry) and
            is_not_duplicate(entry, seen_titles) and
            is_accessible(entry) and
            is_complete(entry)):
            filtered_entries.append(entry)
    
    return filtered_entries

def process_bib_files_in_folder(folder_path, output_file):
    combined_entries = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".bib"):
            file_path = os.path.join(folder_path, file_name)
            bib_database = load_bib_file(file_path)
            combined_entries.extend(bib_database.entries)
    
    num_entries_before = len(combined_entries)
    filtered_entries = filter_entries(combined_entries)
    num_entries_after = len(filtered_entries)
    
    output_database = bibtexparser.bibdatabase.BibDatabase()
    output_database.entries = filtered_entries
    
    save_bib_file(output_database, output_file)
    
    print(f"Number of articles before applying criteria: {num_entries_before}")
    print(f"Number of articles after applying criteria: {num_entries_after}")
    print(f"Filtered articles saved to {output_file}")

if __name__ == "__main__":
    folder_path = "bib_files"  
    output_file = "filtered_articles.bib"
    process_bib_files_in_folder(folder_path, output_file)
