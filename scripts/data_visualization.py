import os
import bibtexparser
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import Levenshtein
import nltk
from nltk.corpus import stopwords

# Download NLTK stop words
nltk.download('stopwords')

def load_bib_file(file_path):
    with open(file_path, encoding='utf-8') as bib_file:
        bib_database = bibtexparser.load(bib_file)
    return bib_database

def save_bib_file(bib_database, output_path):
    with open(output_path, 'w', encoding='utf-8') as bib_file:
        bibtexparser.dump(bib_database, bib_file)

def merge_similar_keywords(keywords, threshold=0.8):
    merged_keywords = {}
    for keyword in keywords:
        merged = False
        for existing_keyword in merged_keywords:
            if Levenshtein.ratio(keyword, existing_keyword) >= threshold:
                merged_keywords[existing_keyword] += keywords[keyword]
                merged = True
                break
        if not merged:
            merged_keywords[keyword] = keywords[keyword]
    return merged_keywords

def get_ngrams(text, n):
    words = text.split()
    ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
    return ngrams

def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    custom_stop_words = {'use', 'also', 'et', 'al', 'one', 'two', 'three'}
    stop_words.update(custom_stop_words)
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

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
    top_n = 20
    all_keywords = []
    for entry in bib_database.entries:
        if 'keywords' in entry:
            all_keywords.extend(entry['keywords'].split(','))
    
    keywords = [keyword.strip().lower() for keyword in all_keywords]
    keyword_counts = Counter(keywords)
    merged_keyword_counts = merge_similar_keywords(keyword_counts, threshold=0.8)
    filtered_keyword_counts = {k: v for k, v in merged_keyword_counts.items() if v >= 5}
    top_keywords = Counter(filtered_keyword_counts).most_common(top_n)
    
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
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(filtered_keyword_counts)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Keywords')
    plt.savefig(os.path.join('images', 'word_cloud.png'))
    plt.close()

    # N-gram analysis from abstracts
    ngram_counts = Counter()
    for entry in bib_database.entries:
        if 'abstract' in entry:
            text = remove_stop_words(entry['abstract'].lower())
            for n in range(1, 4):
                ngram_counts.update(get_ngrams(text, n))
    
    filtered_ngram_counts = {k: v for k, v in ngram_counts.items() if v >= 5}
    top_ngrams = Counter(filtered_ngram_counts).most_common(top_n)
    
    ngrams, counts = zip(*top_ngrams)
    
    plt.figure(figsize=(10, 5))
    plt.barh(ngrams, counts, color='purple')
    plt.xlabel('Frequency')
    plt.ylabel('N-grams')
    plt.title(f'Top {top_n} N-grams from Abstracts')
    plt.gca().invert_yaxis()
    plt.savefig(os.path.join('images', 'top_ngrams.png'))
    plt.close()

if __name__ == "__main__":
    file_path = "filtered_articles.bib"
    bib_database = load_bib_file(file_path)
    visualize_statistics(bib_database)
