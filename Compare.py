import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def kde_plot(npr_csv, qwen_csv, llama_csv, column, output_file):
    # 1. Load your summary CSVs
    npr_df = pd.read_csv(npr_csv)
    qwen_df = pd.read_csv(qwen_csv)
    llama_df = pd.read_csv(llama_csv)

    plt.figure(figsize=(10, 6))

    # 2. Plot both distributions
    sns.kdeplot(data=npr_df[column], fill=True, label='NPR Transcripts (' + str(len(npr_df)) + ')', color='blue', alpha=0.4)
    sns.kdeplot(data=qwen_df[column], fill=True, label='Qwen Transcripts (' + str(len(qwen_df)) + ')', color='orange', alpha=0.4)
    sns.kdeplot(data=llama_df[column], fill=True, label='Llama Transcripts (' + str(len(llama_df)) + ')', color='red', alpha=0.4)

    # 3. Add Vertical Mean Markers
    plt.axvline(npr_df[column].mean(), color='blue', linestyle='--', linewidth=1.5, alpha=0.8)
    plt.axvline(qwen_df[column].mean(), color='orange', linestyle='--', linewidth=1.5, alpha=0.8)
    plt.axvline(llama_df[column].mean(), color='red', linestyle='--', linewidth=1.5, alpha=0.8)

    # 3. Formatting
    plt.title('Comparison of '+ column +' Levels: NPR vs Qwen vs Llama', fontsize=14)
    plt.xlabel(column, fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    plt.savefig('Plots/'+ output_file, dpi=300)
    plt.close()
    print(f"Comparison plot saved as {output_file}")


# mean anxiety
kde_plot('Data/NPR_anxiety.csv',
         'Data/qwen_anxiety.csv',
         'Data/llama_anxiety.csv',
         'Overall_Mean',
         'Anxiety_mean_kde.png',)
kde_plot('Data/NPR_anxiety.csv',
         'Data/qwen_anxiety.csv',
         'Data/llama_anxiety.csv',
         'User_Mean',
         'Anxiety_mean_USER_kde.png',)
kde_plot('Data/NPR_anxiety.csv',
         'Data/qwen_anxiety.csv',
         'Data/llama_anxiety.csv',
         'Asst_Mean',
         'Anxiety_mean_ASST_kde.png',)

kde_plot('Data/NPR_anxiety.csv',
         'Data/qwen_anxiety.csv',
         'Data/llama_anxiety.csv',
         'StandardDeviation',
         'Anxiety_StandardDeviation_kde.png',)


# entropy
kde_plot('Data/NPR_entropy.csv',
         'Data/qwen_entropy.csv',
         'Data/llama_entropy.csv',
         'Entropy',
         'Entropy_kde.png',)
kde_plot('Data/NPR_entropy.csv',
         'Data/qwen_entropy.csv',
         'Data/llama_entropy.csv',
         'User_Entropy',
         'Entropy_User_kde.png',)
kde_plot('Data/NPR_entropy.csv',
         'Data/qwen_entropy.csv',
         'Data/llama_entropy.csv',
         'Assistant_Entropy',
         'Entropy_Assistant_kde.png',)

#distinct_1
kde_plot('Data/NPR_distinct_n.csv',
         'Data/qwen_distinct_n.csv',
         'Data/llama_distinct_n.csv',
         'Distinct_1',
         'Distinct_kde.png',)
kde_plot('Data/NPR_distinct_n.csv',
         'Data/qwen_distinct_n.csv',
         'Data/llama_distinct_n.csv',
         'User_Distinct_1',
         'Distinct_1User_kde.png',)
kde_plot('Data/NPR_distinct_n.csv',
         'Data/qwen_distinct_n.csv',
         'Data/llama_distinct_n.csv',
         'Assistant_Distinct_1',
         'Distinct_1Assistant_kde.png',)




