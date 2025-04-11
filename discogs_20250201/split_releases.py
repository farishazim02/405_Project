import os
import re
import sys
from datetime import datetime

# Settings
input_file = 'discogs_20250201_releases.xml'
output_folder = 'final_csv_outputs'
output_prefix = 'rel_chunk_'
releases_per_file = 2_000_000
checkpoint = 100_000
log_file_path = os.path.join(output_folder, 'split_log.txt')

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Redirect all output to a log file
sys.stdout = open(log_file_path, 'w', encoding='utf-8')

def extract_rel_id(line):
    match = re.search(r'<release id="(\d+)"', line)
    return match.group(1) if match else "Unknown"

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def open_new_file(file_index):
    out_path = os.path.join(output_folder, f"{output_prefix}{file_index}.xml")
    f = open(out_path, 'w', encoding='utf-8')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<releases>\n')
    print(f"[{get_timestamp()}] Starting File {file_index}: {output_prefix}{file_index}.xml")
    return f

# Start timing
start_time = datetime.now()
file_idx = 1
release_count = 0
file_release_count = 0
current_file = open_new_file(file_idx)

with open(input_file, 'r', encoding='utf-8') as infile:
    for line in infile:
        if '<release' in line:
            release_block = [line]
            while True:
                next_line = infile.readline()
                if not next_line:
                    break
                release_block.append(next_line)
                if '</release>' in next_line:
                    break

            file_release_count += 1
            release_count += 1
            rel_id = extract_rel_id(release_block[0])
            current_file.writelines(release_block)

            if file_release_count % checkpoint == 0:
                elapsed = datetime.now() - start_time
                print(f"[{get_timestamp()}] Checkpoint: File {file_idx} - {file_release_count} releases written, last rel_id: {rel_id} - Total: {release_count} (Elapsed: {elapsed})")

            if file_release_count >= releases_per_file:
                current_file.write('</releases>\n')
                current_file.close()
                elapsed = datetime.now() - start_time
                print(f"[{get_timestamp()}] Completed File {file_idx} with {file_release_count} releases, last rel_id: {rel_id} (Elapsed: {elapsed})")
                file_idx += 1
                file_release_count = 0
                current_file = open_new_file(file_idx)

# Final file closing
if current_file and not current_file.closed:
    current_file.write('</releases>\n')
    current_file.close()
    elapsed = datetime.now() - start_time
    print(f"[{get_timestamp()}] Completed FINAL File {file_idx} with {file_release_count} releases (Elapsed: {elapsed})")

print(f"[{get_timestamp()}] ✅ Total releases processed: {release_count}")
