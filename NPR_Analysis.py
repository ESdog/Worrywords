import csv
import glob
import os
import AnxietyAnalysis as anx

transcript_dir = r'Data/npr-transcripts/'
output_dir = r'Data/analysis-results/'
output_file = r'Data/NPR_anxiety_summary.csv'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get list of all matching files (handles missing numbers automatically)
transcript_files = glob.glob(os.path.join(transcript_dir, "episode-*.txt"))
print(f"Found {len(transcript_files)} transcripts. Starting analysis...")

word_scores = anx.build_anxiety_map()

# Open the output file in write mode
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    # Define the header for your data
    fieldnames = ['Episode', 'MeanAnxiety', 'Density', 'WordCount', 'AnxietyHits', 'StandardDeviation']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    print(f"Analyzing {len(transcript_files)} transcripts...")

    for file_path in transcript_files:
        base_name = os.path.basename(file_path).replace('.txt', '')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # Evaluate using your existing function
            results = anx.get_anxiety_distribution(text, word_scores)

            if isinstance(results, anx.AnxietyResults):
                # Write a row of data for this episode
                writer.writerow({
                    'Episode': base_name,
                    'MeanAnxiety': round(results.mean_anxiety, 4),
                    'Density': round(results.density, 4),
                    'WordCount': results.word_count,
                    'AnxietyHits': results.anxiety_hits,
                    'StandardDeviation': results.std_dev_anxiety
                })
        except Exception as e:
            print(f"Error on {base_name}: {e}")

print(f"All scores saved to: {output_file}")




