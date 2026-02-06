import csv
import glob
import os
import AnxietyAnalysis as anx

npr_output_dir = r'Data/NPR_anxiety.csv'
qwen_output_dir = r'Data/qwen_anxiety.csv'
llama_output_dir = r'Data/llama_anxiety.csv'
psyc_output_dir = r'Data/psyc_anxiety.csv'

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

anxiety_word_scores = anx.build_anxiety_map()


def analyze_anxiety_parallel(transcript_files, output_file, word_scores):
    # Expanded fieldnames for both speakers
    fieldnames = [
        'Episode',
        'User_Mean', 'User_Density', 'User_WordCount',
        'Asst_Mean', 'Asst_Density', 'Asst_WordCount',
        'Overall_Mean', 'StandardDeviation', 'Density', 'WordCount',
    ]

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
                            if line.startswith(('User:', 'Host:')):
                                user_lines.append(line.split(':', 1)[-1].strip())
                            elif line.startswith(('Assistant:', 'Guest:')):
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
analyze_anxiety_parallel(qwen_files, qwen_output_dir, anxiety_word_scores)
analyze_anxiety_parallel(llama_files, llama_output_dir, anxiety_word_scores)
analyze_anxiety_parallel(psyc_files, psyc_output_dir, anxiety_word_scores)
