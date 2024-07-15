import os
import bibtexparser
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

def load_bib_file(file_path):
    with open(file_path, encoding='utf-8') as bib_file:
        bib_database = bibtexparser.load(bib_file)
    return bib_database

def visualize_statistics(bib_database):
    # Create directory for images if it doesn't exist
    os.makedirs('images', exist_ok=True)

    # Distribution of articles by year
    years = [int(entry['year']) for entry in bib_database.entries if 'year' in entry]
    year_counts = Counter(years)
    years, counts = zip(*sorted(year_counts.items()))
    
    plt.figure(figsize=(10, 5))
    plt.bar(years, counts, color='blue')
    plt.xlabel('Year')
    plt.ylabel('Number of Articles')
    plt.title('Distribution of Articles by Year')
    plt.savefig(os.path.join('images', 'distribution_by_year.png'))
    plt.close()

    # Top N keywords
    top_n = 10
    all_keywords = []
    for entry in bib_database.entries:
        if 'keywords' in entry:
            all_keywords.extend(entry['keywords'].split(','))
    
    keywords = [keyword.strip().lower() for keyword in all_keywords]
    keyword_counts = Counter(keywords)
    top_keywords = keyword_counts.most_common(top_n)
    
    keywords, counts = zip(*top_keywords)
    
    plt.figure(figsize=(10, 5))
    plt.barh(keywords, counts, color='green')
    plt.xlabel('Frequency')
    plt.ylabel('Keywords')
    plt.title(f'Top {top_n} Keywords')
    plt.gca().invert_yaxis()
    plt.savefig(os.path.join('images', 'top_keywords.png'))
    plt.close()

    # Word cloud for keywords
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(keywords))
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Keywords')
    plt.savefig(os.path.join('images', 'word_cloud.png'))
    plt.close()

if __name__ == "__main__":
    file_path = "filtered_articles.bib"
    bib_database = load_bib_file(file_path)
    visualize_statistics(bib_database)
