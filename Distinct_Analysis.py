import math
from collections import Counter
import csv
import glob
import os

npr_output_dir = r'Data/NPR_distinct_n.csv'
qwen_output_dir = r'Data/qwen_distinct_n.csv'
llama_output_dir = r'Data/llama_distinct_n.csv'
psyc_output_dir = r'Data/psyc_distinct_n.csv'

# Setup paths
npr_dir = r'Data/npr-transcripts'
qwen_dir = r'Data/qwen30transcripts/'
llama_dir = r'Data/llama-transcripts'
psyc_dir = r'Data/psyc-transcripts'


# Get list of all matching files (handles missing numbers automatically)
npr_files = glob.glob(os.path.join(npr_dir, "episode-*.txt"))
qwen_files = glob.glob(os.path.join(qwen_dir, "DM_*_Interview.txt"))
llama_files = glob.glob(os.path.join(llama_dir, "DM_*_Interview.txt"))
psyc_files = glob.glob(os.path.join(psyc_dir, "*_P.txt"))


def calculate_distinct_1(text):
    """Calculates the ratio of unique words to total words."""
    tokens = text.lower().split()  # Simple tokenization
    if not tokens:
        return 0

    unique_tokens = set(tokens)
    return len(unique_tokens) / len(tokens)



# def analyze_transcripts_to_csv(transcript_files, output_file):
#     fieldnames = ['Episode', 'Distinct-1']
#
#     try:
#         with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#
#             for file_path in transcript_files:
#                 base_name = os.path.basename(file_path).replace('.txt', '')
#                 try:
#                     with open(file_path, 'r', encoding='utf-8') as f:
#                         full_text = f.read()
#
#                     text = full_text.split('<STOP>')[0].strip()
#                     score = calculate_distinct_1(text)
#                     writer.writerow({
#                         'Episode': base_name,
#                         'Distinct-1': score
#                     })
#                 except Exception as e:
#                     print(f"Error on {base_name}: {e}")
#
#         print(f"Scores saved to: {output_file}")
#
#     except IOError as e:
#         print(f"Could not write to file {output_file}: {e}")


def analyze_transcripts_to_csv(transcript_files, output_file):
    # Added 'Overall_Distinct_1' to headers
    fieldnames = ['Episode', 'User_Distinct_1', 'Assistant_Distinct_1', 'Distinct_1']

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for file_path in transcript_files:
                base_name = os.path.basename(file_path).replace('.txt', '')

                user_lines = []
                assistant_lines = []

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if '<STOP>' in line:
                                break

                            if line.startswith('User:') | line.startswith('Guest:'):
                                user_lines.append(line.replace('User:', '').strip())
                            elif line.startswith('Assistant:') | line.startswith('Host:'):
                                assistant_lines.append(line.replace('Assistant:', '').strip())

                    # Combine lines into full strings
                    user_text = " ".join(user_lines)
                    assistant_text = " ".join(assistant_lines)
                    if not user_text and not assistant_text:
                        overall_text = line
                    else:
                        overall_text = user_text + " " + assistant_text

                    # Calculate all three metrics
                    writer.writerow({
                        'Episode': base_name,
                        'User_Distinct_1': calculate_distinct_1(user_text),
                        'Assistant_Distinct_1': calculate_distinct_1(assistant_text),
                        'Distinct_1': calculate_distinct_1(overall_text)
                    })

                except Exception as e:
                    print(f"Error processing {base_name}: {e}")

        print(f"Parallel and Overall analysis saved to: {output_file}")

    except IOError as e:
        print(f"Could not write to file {output_file}: {e}")


analyze_transcripts_to_csv(npr_files, npr_output_dir)
analyze_transcripts_to_csv(qwen_files, qwen_output_dir)
analyze_transcripts_to_csv(llama_files, llama_output_dir)
analyze_transcripts_to_csv(psyc_files, psyc_output_dir)