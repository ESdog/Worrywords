import math
from collections import Counter
import csv
import glob
import os

npr_output_dir = r'Data/NPR_entropy.csv'
qwen_output_dir = r'Data/qwen_entropy.csv'
llama_output_dir = r'Data/llama_entropy.csv'

# Setup paths
npr_dir = r'Data/npr-transcripts'
qwen_dir = r'Data/qwen30transcripts/'
llama_dir = r'Data/llama-transcripts'


# Get list of all matching files (handles missing numbers automatically)
npr_files = glob.glob(os.path.join(npr_dir, "episode-*.txt"))
qwen_files = glob.glob(os.path.join(qwen_dir, "DM_*_Interview.txt"))
llama_files = glob.glob(os.path.join(llama_dir, "DM_*_Interview.txt"))

def calculate_normalized_entropy(text):
    if not text: return 0

    # 1. Frequency calculation
    counts = Counter(text)
    total_symbols = len(text)
    probs = [count / total_symbols for count in counts.values()]

    # 2. Shannon Entropy
    shannon_entropy = -sum(p * math.log2(p) for p in probs)

    # 3. Normalization
    # Maximum possible entropy is log2 of the number of unique symbols
    max_entropy = math.log2(len(counts)) if len(counts) > 1 else 1

    return shannon_entropy / max_entropy



# def analyze_transcripts_to_csv(transcript_files, output_file):
#     """
#     Analyzes a list of transcript files for anxiety scores and normalized entropy,
#     saving the results to a specified CSV file.
#     """
#     # Define the header including the new Entropy column
#     fieldnames = [
#         'Episode', 'Entropy'
#     ]
#
#     try:
#         with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#
#             print(f"Analyzing {len(transcript_files)} transcripts...")
#
#             for file_path in transcript_files:
#                 base_name = os.path.basename(file_path).replace('.txt', '')
#
#                 try:
#                     with open(file_path, 'r', encoding='utf-8') as f:
#                         full_text = f.read()
#
#                     text = full_text.split('<STOP>')[0].strip()
#                     # print(calculate_normalized_entropy(text))
#                     result = calculate_normalized_entropy(text)
#                     if result > 0:
#                         # Write a row of data for this episode
#                         writer.writerow({
#                             'Episode': base_name,
#                             'Entropy': result
#                         })
#
#                 except Exception as e:
#                     print(f"Error on {base_name}: {e}")
#
#         print(f"All scores successfully saved to: {output_file}")
#
#     except IOError as e:
#         print(f"Could not write to file {output_file}: {e}")

def analyze_transcripts_to_csv(transcript_files, output_file):
    # Parallel headers for Entropy
    fieldnames = ['Episode', 'User_Entropy', 'Assistant_Entropy', 'Entropy']

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for file_path in transcript_files:
                base_name = os.path.basename(file_path).replace('.txt', '')

                user_side = []  # For User: or Host:
                assistant_side = []  # For Assistant: or Guest:

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if '<STOP>' in line:
                                break

                            # Check for User or Host
                            if line.startswith('User:') | line.startswith('Guest:'):
                                clean = line.split(':', 1)[1].strip()
                                user_side.append(clean)
                            # Check for Assistant or Guest
                            elif line.startswith('Assistant:') | line.startswith('Host:'):
                                clean = line.split(':', 1)[1].strip()
                                assistant_side.append(clean)

                    u_text = " ".join(user_side)
                    a_text = " ".join(assistant_side)
                    o_text = u_text + " " + a_text

                    writer.writerow({
                        'Episode': base_name,
                        'User_Entropy': calculate_normalized_entropy(u_text),
                        'Assistant_Entropy': calculate_normalized_entropy(a_text),
                        'Entropy': calculate_normalized_entropy(o_text)
                    })

                except Exception as e:
                    print(f"Error on {base_name}: {e}")

        print(f"Entropy scores saved to: {output_file}")

    except IOError as e:
        print(f"Could not write to file {output_file}: {e}")

analyze_transcripts_to_csv(npr_files, npr_output_dir)
analyze_transcripts_to_csv(qwen_files, qwen_output_dir)
analyze_transcripts_to_csv(llama_files, llama_output_dir)