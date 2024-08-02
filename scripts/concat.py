import os
import bibtexparser

def load_bib_file(file_path):
    with open(file_path, encoding='utf-8') as bib_file:
        return bibtexparser.load(bib_file)

def save_bib_file(bib_database, output_path):
    with open(output_path, 'w', encoding='utf-8') as bib_file:
        bibtexparser.dump(bib_database, bib_file)

def is_not_duplicate(entry, seen_dois, seen_titles):
    doi = entry.get('doi', '').strip().lower()
    title = entry.get('title', '').strip().lower()
    
    if doi:
        if doi in seen_dois:
            return False
        seen_dois.add(doi)
    else:
        if title in seen_titles:
            return False
        seen_titles.add(title)
    
    return True

def process_bib_files_in_folder(folder_path, output_file):
    combined_entries = []
    seen_dois = set()
    seen_titles = set()
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".bib") and os.path.isfile(file_path):
            bib_database = load_bib_file(file_path)
            combined_entries.extend(bib_database.entries)
    
    num_entries_before = len(combined_entries)
    
    unique_entries = []
    for entry in combined_entries:
        if is_not_duplicate(entry, seen_dois, seen_titles):
            unique_entries.append(entry)
    
    num_entries_after = len(unique_entries)
    
    output_database = bibtexparser.bibdatabase.BibDatabase()
    output_database.entries = unique_entries
    
    save_bib_file(output_database, output_file)
    
    print(f"Number of articles before removing duplicates: {num_entries_before}")
    print(f"Number of articles after removing duplicates: {num_entries_after}")
    print(f"Consolidated articles saved to {output_file}")

if __name__ == "__main__":
    folder_path = "./bib_files/SQ1+SQ2+SQ3+SQ4"  # Replace with your .bib files directory path
    output_file = "final_articles.bib"
    process_bib_files_in_folder(folder_path, output_file)
