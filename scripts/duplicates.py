import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import os

def load_bib_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as bib_file:
        return bibtexparser.load(bib_file)



def remove_duplicates(bib_files):
    seen_dois = set()
    seen_titles = set()
    unique_entries = []
    total_entries = 0
    
    for bib_file in bib_files:
        bib_data = load_bib_file(bib_file)
        total_entries += len(bib_data.entries)
        for entry in bib_data.entries:
            doi = entry.get('doi', '').strip().lower()
            title = entry.get('title', '').strip().lower()
            
            if doi and doi not in seen_dois:
                seen_dois.add(doi)
                unique_entries.append(entry)
            elif not doi and title not in seen_titles:
                seen_titles.add(title)
                unique_entries.append(entry)
    
    return unique_entries, total_entries

def main():
    folder_path = './bib_files/SQ1' 
    
    # List all .bib files in the folder
    bib_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.bib')]
    
    if not bib_files:
        print("No .bib files found in the specified folder.")
        return
    
    # Remove duplicates
    unique_entries, total_entries = remove_duplicates(bib_files)
    
    print(f"Total entries before removing duplicates: {total_entries}")
    print(f"Total entries after removing duplicates: {len(unique_entries)}")


if __name__ == '__main__':
    main()
