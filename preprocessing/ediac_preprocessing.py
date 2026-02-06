import glob
import os
from pathlib import Path

# input_dir = r'Data/ediac-transcripts'
# output_dir = r'Data/psyc-transcripts'
#
#
# pattern = os.path.join(input_dir, "*_P.txt")
#
# psyc_files = glob.glob(pattern)
#
# print(f"Found {len(psyc_files)} files to process")
#
# marker = "FULL TRANSCRIPTION:"
#
# for file_path in psyc_files:
#     with open(file_path, "r", encoding="utf-8") as f:
#         text = f.read()
#         # Split and extract after marker
#
#     parts = text.split(marker, 1)
#     if len(parts) > 1:
#         full_transcription = parts[1].strip()
#
#         # Create output filename (same name, new directory)
#         output_file = os.path.join(output_dir, os.path.basename(file_path))
#
#         with open(output_file, "w", encoding="utf-8") as f:
#             f.write(full_transcription)
#
#         print(f"Processed: {os.path.basename(file_path)} -> {output_dir}")
#     else:
#         print(f"Warning: Marker not found in {file_path}")
#
#
# print(f"Processed {len(psyc_files)} files")

input_dir = Path("Data/ediac-transcripts")
output_dir = Path("Data/psyc-transcripts")
# output_dir.mkdir(exist_ok=True)

marker = "FULL TRANSCRIPTION:"

processed = 0
for i in range(300, 652):  # 300 to 651 inclusive
    filename = f"{i}_P.txt"
    file_path = input_dir / filename

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        parts = text.split(marker, 1)
        if len(parts) > 1:
            full_transcription = parts[1].strip()
            output_file = output_dir / filename

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(full_transcription)

            print(f"✓ {filename}")
            processed += 1
        else:
            print(f"✗ {filename} (no marker)")
    else:
        print(f"- {filename} (missing)")

print(f"\nProcessed {processed} files")
