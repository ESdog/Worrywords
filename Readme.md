## Overview
Analyzing the texts like transcripts/radio interviews for objective analytical overview
### Key Features
*   **Word-to-Anxiety Mapping:** Anxiety intensity scoring.
*   **Statistical Analysis:** Calculating entropy, and various anxiety score metrics
*   **Visualization:** Fixed-bin histograms and Comparative KDE plots.

## 📂 Directory Structure
```text
WorryWords/
├── Data/
│   ├── npr-transcripts/       # Source .txt files (episode-*.txt)
│   ├── Llama-transcripts/      # AI-generated transcripts
│   └── qwen30-transcripts/      # AI-generated transcripts
├── Plots/                     # Generated histograms and KDE comparison charts
├── Data/
│   ├── worrywords-v1.txt      # The anxiety score reference dictionary
└── Other python scripts for analysis           
