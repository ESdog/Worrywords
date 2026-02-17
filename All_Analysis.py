import csv
import glob
import os
from collections import Counter
import math
import AnxietyAnalysis as anx

npr_output_dir = r'Data/NPR'
qwen_output_dir = r'Data/qwen'
llama_output_dir = r'Data/llama'
psyc_output_dir = r'Data/psyc'
synth_output_dir = r'Data/synth'
spitv2_output_dir = r'Data/spitv2'

# Setup paths
npr_dir = r'Data/npr-transcripts'
qwen_dir = r'Data/qwen30transcripts/'
llama_dir = r'Data/llama-transcripts'
psyc_dir = r'Data/psyc-transcripts'
synth_dir = r'Data/synthetic-transcripts'
spitv2_dir = r'Data/spitv2-transcripts'


# Get list of all matching files (handles missing numbers automatically)
npr_files = glob.glob(os.path.join(npr_dir, "episode-*.txt"))
qwen_files = glob.glob(os.path.join(qwen_dir, "DM_*_Interview.txt"))
llama_files = glob.glob(os.path.join(llama_dir, "DM_*_Interview.txt"))
psyc_files = glob.glob(os.path.join(psyc_dir, "*_P.txt"))
synth_files = glob.glob(os.path.join(synth_dir, "*.txt"))
spitv2_files = glob.glob(os.path.join(spitv2_dir, "*.txt"))



###---HELPERS---###
anxiety_word_scores = anx.build_anxiety_map()

def calculate_distinct_1(text):
    """Calculates the ratio of unique words to total words."""
    tokens = text.lower().split()  # Simple tokenization
    if not tokens:
        return 0

    unique_tokens = set(tokens)
    return len(unique_tokens) / len(tokens)


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



def analyze_transcripts_entropy_to_csv(transcript_files, output):
    # Parallel headers for Entropy
    fieldnames = ['Episode', 'User_Entropy', 'Assistant_Entropy', 'Entropy']
    output_file = output + '_entropy.csv'

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
                            if line.startswith('User:') | line.startswith('Guest:') | line.startswith('patient:'):
                                clean = line.split(':', 1)[1].strip()
                                user_side.append(clean)
                            # Check for Assistant or Guest
                            elif line.startswith('Assistant:') | line.startswith('Host:') | line.startswith('interviewer:'):
                                clean = line.split(':', 1)[1].strip()
                                assistant_side.append(clean)

                    u_text = " ".join(user_side)
                    a_text = " ".join(assistant_side)
                    if not u_text and not a_text:
                        o_text = line
                    else:
                        o_text = u_text + " " + a_text
                    # o_text = u_text + " " + a_text

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

def analyze_transcripts_distinct_to_csv(transcript_files, output):
    # Added 'Overall_Distinct_1' to headers
    fieldnames = ['Episode', 'User_Distinct_1', 'Assistant_Distinct_1', 'Distinct_1']
    output_file = output + '_distinct_n.csv'

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

                            if line.startswith('User:') | line.startswith('Guest:') | line.startswith('patient:'):
                                user_lines.append(line.replace('User:', '').strip())
                            elif line.startswith('Assistant:') | line.startswith('Host:') | line.startswith('interviewer:'):
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



def analyze_anxiety_parallel(transcript_files, output, word_scores):
    # Expanded fieldnames for both speakers
    fieldnames = [
        'Episode',
        'User_Mean', 'User_Density', 'User_WordCount',
        'Asst_Mean', 'Asst_Density', 'Asst_WordCount',
        'Overall_Mean', 'StandardDeviation', 'Density', 'WordCount',
    ]
    output_file = output + '_anxiety.csv'

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for file_path in transcript_files:
                base_name = os.path.basename(file_path).replace('.txt', '')

                user_lines = []
                asst_lines = []

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if '<STOP>' in line:
                                break

                            # Support both User/Host and Assistant/Guest labels
                            if line.startswith(('User:', 'Host:', 'patient:')):
                                user_lines.append(line.split(':', 1)[-1].strip())
                            elif line.startswith(('Assistant:', 'Guest:', 'interviewer:')):
                                asst_lines.append(line.split(':', 1)[-1].strip())

                    # Prepare text blocks
                    user_text = " ".join(user_lines)
                    asst_text = " ".join(asst_lines)
                    if not user_text and not asst_text:
                        overall_text = line
                    else:
                        overall_text = user_text + " " + asst_text

                    # Run your AnxietyAnalysis functions
                    u_res = anx.get_anxiety_distribution(user_text, word_scores)
                    a_res = anx.get_anxiety_distribution(asst_text, word_scores)
                    o_res = anx.get_anxiety_distribution(overall_text, word_scores)

                    writer.writerow({
                        'Episode': base_name,
                        # User Stats
                        'User_Mean': round(u_res.mean_anxiety, 4) if u_res else 0,
                        'User_Density': round(u_res.density, 4) if u_res else 0,
                        'User_WordCount': u_res.word_count if u_res else 0,
                        # Assistant Stats
                        'Asst_Mean': round(a_res.mean_anxiety, 4) if a_res else 0,
                        'Asst_Density': round(a_res.density, 4) if a_res else 0,
                        'Asst_WordCount': a_res.word_count if a_res else 0,
                        # Combined Metric
                        'Overall_Mean': round(o_res.mean_anxiety, 4) if o_res else 0,
                        'StandardDeviation': o_res.std_dev_anxiety if o_res else 0,
                        'Density': round(o_res.density, 4) if o_res else 0,
                        'WordCount': o_res.word_count if o_res else 0,
                    })

                except Exception as e:
                    print(f"Error on {base_name}: {e}")

        print(f"Anxiety analysis successfully saved to: {output_file}")

    except IOError as e:
        print(f"Could not write to file {output_file}: {e}")


analyze_anxiety_parallel(npr_files, npr_output_dir, anxiety_word_scores)
analyze_transcripts_distinct_to_csv(npr_files, npr_output_dir)
analyze_transcripts_entropy_to_csv(npr_files, npr_output_dir)

analyze_anxiety_parallel(qwen_files, qwen_output_dir, anxiety_word_scores)
analyze_transcripts_distinct_to_csv(qwen_files, qwen_output_dir)
analyze_transcripts_entropy_to_csv(qwen_files, qwen_output_dir)

analyze_anxiety_parallel(llama_files, llama_output_dir, anxiety_word_scores)
analyze_transcripts_distinct_to_csv(llama_files, llama_output_dir)
analyze_transcripts_entropy_to_csv(llama_files, llama_output_dir)

analyze_anxiety_parallel(psyc_files, psyc_output_dir, anxiety_word_scores)
analyze_transcripts_distinct_to_csv(psyc_files, psyc_output_dir)
analyze_transcripts_entropy_to_csv(psyc_files, psyc_output_dir)

analyze_anxiety_parallel(synth_files, synth_output_dir, anxiety_word_scores)
analyze_transcripts_distinct_to_csv(synth_files, synth_output_dir)
analyze_transcripts_entropy_to_csv(synth_files, synth_output_dir)

analyze_anxiety_parallel(spitv2_files, spitv2_output_dir, anxiety_word_scores)
analyze_transcripts_distinct_to_csv(spitv2_files, spitv2_output_dir)
analyze_transcripts_entropy_to_csv(spitv2_files, spitv2_output_dir)