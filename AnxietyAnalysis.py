import csv
import re
import statistics
import matplotlib.pyplot as plt
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict
import statistics

@dataclass
class AnxietyResults:
    word_count: int
    anxiety_hits: int
    mean_anxiety: float
    std_dev_anxiety: float
    density: float
    #score_distribution: Dict[float, int] = field(repr=False) # Hides long score lists when printing
    #scores: List[float] = field(repr=False) # Hides long score lists when printing

# Standardized Path Constant
WORRYWORDS_PATH = r'WorryWords\worrywords-v1.txt'

def build_anxiety_map(filepath=WORRYWORDS_PATH):
    """
    Builds the map. Defaults to the standardized WORRYWORDS_PATH
    unless a different path is provided.
    """
    anxiety_map = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            anxiety_map[row['Term'].lower()] = float(row['Mean'])
    return anxiety_map


def get_anxiety_distribution(text, anxiety_map):
    words = re.findall(r'\b\w+\b', text.lower())
    found_scores = [anxiety_map[w] for w in words if w in anxiety_map]

    if not found_scores:
        return None

    return AnxietyResults(
        word_count=len(words),
        anxiety_hits=len(found_scores),
        mean_anxiety=statistics.mean(found_scores),
        std_dev_anxiety=statistics.stdev(found_scores) if len(found_scores) > 1 else 0.0,
        density=sum(found_scores) / len(words),
        #score_distribution=dict(Counter(found_scores)),
        #scores=found_scores
    )


def plot_anxiety_histogram(stats, filename):
    dist = stats["scores"]
    custom_bins = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]

    plt.figure(figsize=(10, 12))
    plt.hist(dist, bins=custom_bins, color='skyblue', edgecolor='black', alpha=0.7)
    plt.yscale('log')
    plt.title('Anxiety Score Distribution (Fixed Bins)')
    plt.xlabel('Anxiety Intensity')
    plt.ylabel('Frequency (Log Word Count)')
    plt.xticks(custom_bins)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Histogram saved as {filename}")
