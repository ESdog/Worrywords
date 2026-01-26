import csv
import re
from collections import Counter
import time
import matplotlib.pyplot as plt

worrywords_v1 = r'D:\work\PycharmProjects\WorryWords\WorryWords\worrywords-v1.txt'
input_file_path = r'D:\work\PycharmProjects\WorryWords\Data\Episode-1.txt'

def build_anxiety_map(filepath):
    anxiety_map = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        # Uses 'excel-tab' dialect to automatically handle the tab spacing
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            # Map 'Term' to its numerical 'Mean' score
            anxiety_map[row['Term'].lower()] = float(row['Mean'])
    return anxiety_map

# Usage
word_scores = build_anxiety_map(worrywords_v1)

def plot_from_stats(stats, filename):
    dist = stats["scores"]

    custom_bins = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]

    plt.figure(figsize=(10, 12))
    # This automatically 'counts' how many scores fall into each bin
    plt.hist(dist, bins=custom_bins, color='skyblue', edgecolor='black', alpha=0.7)

    # 3. Format the chart
    plt.title('Anxiety Score Distribution (Fixed Bins)')
    plt.xlabel('Anxiety Intensity')
    plt.yscale('log')
    plt.ylabel('Frequency (Word Count)')

    # Force the x-axis to show your exact bin edges
    plt.xticks(custom_bins)

    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 4. Save and close
    plt.savefig('D:\\work\\PycharmProjects\\WorryWords\\Plots\\' + filename, dpi=300, bbox_inches='tight')
    plt.close()  # Recommended to free up memory if running multiple times
    print(f"Histogram saved as {filename}")

def get_anxiety_distribution(text, anxiety_map):
    # Standardize text and extract words
    words = re.findall(r'\b\w+\b', text.lower())

    found_scores = []
    for word in words:
        if word in anxiety_map:
            found_scores.append(anxiety_map[word])

    if not found_scores:
        return "No anxiety-related terms found."

    # Generate distribution and statistics
    stats = {
        "word_count": len(words),
        "anxiety_hits": len(found_scores),
        "mean_anxiety": sum(found_scores) / len(found_scores),
        "density": sum(found_scores) / len(words),  # Score normalized by text length
        "score_distribution": dict(Counter(found_scores)),
        "scores": found_scores,
    }
    return stats


# Example Usage
my_text = "The panicked survivors feared an impending apocalypse."
results = get_anxiety_distribution(my_text, word_scores)
plot_from_stats(results, "sentence")
print("one line: ", results)


# Read the entire file into a variable
try:
    with open(input_file_path, 'r', encoding='utf-8') as f:
        # .read() loads the whole file as one large string
        text_to_analyze = f.read()
except FileNotFoundError:
    print(f"Error: The file at {input_file_path} was not found.")
    text_to_analyze = ""

if text_to_analyze != "":
    start_time = time.perf_counter()
    results2 = get_anxiety_distribution(text_to_analyze, word_scores)
    end_time = time.perf_counter()
    plot_from_stats(results2,"interview")
    print("NPR interview 1: ", results2)




