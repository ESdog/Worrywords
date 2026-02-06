import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

comp_colors = [
    "blue",
    "orange",
    "green",
    "red",
    "purple",
    "brown",
    "pink",
    "gray",
]

comp_labels = ['NPR Transcripts', 'Qwen Transcripts', 'Llama Transcripts', 'Psyc int. transcripts']

def kde_plot(csv_paths, labels, colors, column, title, output_file):
    """
    csv_paths: list of CSV file paths
    labels:    list of label strings (same length as csv_paths)
    colors:    list of colors (same length as csv_paths)
    column:    column name to plot
    title:     plot title
    output_file: filename (inside Plots/)
    """
    plt.figure(figsize=(10, 6))

    for path, label, color in zip(csv_paths, labels, colors):
        df = pd.read_csv(path)
        sns.kdeplot(
            data=df[column],
            fill=True,
            label=f"{label} ({len(df)})",
            color=color,
            alpha=0.4
        )
        plt.axvline(
            df[column].mean(),
            color=color,
            linestyle='--',
            linewidth=1.5,
            alpha=0.8
        )

    plt.title(title, fontsize=14)
    plt.xlabel(column, fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    plt.savefig('Plots/' + output_file, dpi=300)
    plt.close()
    print(f"Comparison plot saved as {output_file}")

csvs_anxiety = [
    'Data/NPR_anxiety.csv',
    'Data/qwen_anxiety.csv',
    'Data/llama_anxiety.csv',
    'Data/psyc_anxiety.csv'
]

csvs_entropy = [
    'Data/NPR_entropy.csv',
    'Data/qwen_entropy.csv',
    'Data/llama_entropy.csv',
    'Data/psyc_entropy.csv'
]

csvs_distinct_n = ['Data/NPR_distinct_n.csv',
                   'Data/qwen_distinct_n.csv',
                   'Data/llama_distinct_n.csv',
                   'Data/psyc_distinct_n.csv'
]


# mean anxiety
kde_plot(
    csv_paths=csvs_anxiety,
    labels=comp_labels,
    colors=comp_colors,
    column='Overall_Mean',
    title='Comparison of Overall Mean Levels',
    output_file='Anxiety_mean_kde.png'
)
kde_plot(
    csv_paths=csvs_anxiety,
    labels=comp_labels,
    colors=comp_colors,
    column='User_Mean',
    title='Comparison of User Mean Levels',
    output_file='Anxiety_mean_USER_kde.png'
)
kde_plot(
    csv_paths=csvs_anxiety,
    labels=comp_labels,
    colors=comp_colors,
    column='Asst_Mean',
    title='Comparison of Assistant Mean Levels',
    output_file='Anxiety_mean_ASST_kde.png'
)
kde_plot(
    csv_paths=csvs_anxiety,
    labels=comp_labels,
    colors=comp_colors,
    column='StandardDeviation',
    title='Comparison of Standard Deviation Levels',
    output_file='Anxiety_StandardDeviation_kde.png'
)


# entropy
kde_plot(
    csv_paths=csvs_entropy,
    labels=comp_labels,
    colors=comp_colors,
    column='Entropy',
    title='Comparison of Entropy Levels',
    output_file='Entropy_kde.png'
)
kde_plot(
    csv_paths=csvs_entropy,
    labels=comp_labels,
    colors=comp_colors,
    column='User_Entropy',
    title='Comparison of User Entropy Levels',
    output_file='Entropy_User_kde.png'
)
kde_plot(
    csv_paths=csvs_entropy,
    labels=comp_labels,
    colors=comp_colors,
    column='Assistant_Entropy',
    title='Comparison of Assistant Entropy Levels',
    output_file='Entropy_Assistant_kde.png'
)

# distinct_1
kde_plot(
    csv_paths=csvs_distinct_n,
    labels=comp_labels,
    colors=comp_colors,
    column='Distinct_1',
    title='Comparison of Distinct-1 Levels',
    output_file='Distinct_kde.png'
)
kde_plot(
    csv_paths=csvs_distinct_n,
    labels=comp_labels,
    colors=comp_colors,
    column='User_Distinct_1',
    title='Comparison of User Distinct-1 Levels',
    output_file='Distinct_1User_kde.png'
)
kde_plot(
    csv_paths=csvs_distinct_n,
    labels=comp_labels,
    colors=comp_colors,
    column='Assistant_Distinct_1',
    title='Comparison of Assistant Distinct-1 Levels',
    output_file='Distinct_1Assistant_kde.png'
)




