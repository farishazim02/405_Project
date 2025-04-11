import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

# Define the logging function to print to console and write to log file.
LOG_FILE = 'extract_csv_log.txt'
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE, 'a', encoding='utf-8') as logf:
        logf.write(full_message + "\n")

def parse_master(master_elem):
    """
    Extracts information from a <master> element.
    Returns a dictionary with the following keys:
      master_id, title, main_release, genres, styles, year, artist
    """
    master_id = master_elem.get('id', '').strip()
    title = (master_elem.findtext("title") or "").strip()
    main_release = (master_elem.findtext("main_release") or "").strip()
    
    # Extract genres and styles as comma-separated strings
    genres = [g.text.strip() for g in master_elem.findall("genres/genre") if g.text]
    styles = [s.text.strip() for s in master_elem.findall("styles/style") if s.text]
    year = (master_elem.findtext("year") or "").strip()
    
    # Extract the first artist name (if available)
    artist_node = master_elem.find("artists/artist/name")
    artist = artist_node.text.strip() if artist_node is not None and artist_node.text else ""
    
    return {
        'master_id': master_id,
        'title': title,
        'main_release': main_release,
        'genres': ', '.join(genres),
        'styles': ', '.join(styles),
        'year': year,
        'artist': artist
    }

def parse_masters_xml(xml_file_path):
    """
    Parses the masters XML file and extracts the desired fields from each <master> element.
    Prints progress messages every 100,000 masters.
    Returns a DataFrame of all extracted records.
    """
    context = ET.iterparse(xml_file_path, events=('end',))
    _, root = next(context)  # Grab the root element
    records = []
    count = 0

    for event, elem in context:
        if elem.tag == 'master':
            record = parse_master(elem)
            records.append(record)
            count += 1

            if count % 100000 == 0:
                log_message(f"Processed {count:,} masters; current master id: {record['master_id']}")

            elem.clear()
            root.clear()
    
    log_message(f"Finished parsing {count:,} masters.")
    return pd.DataFrame(records)

def main():
    input_xml_path = 'discogs_20250201_masters.xml'
    output_folder = 'final_csv_outputs'
    os.makedirs(output_folder, exist_ok=True)
    output_csv_path = os.path.join(output_folder, 'masters_summary.csv')

    log_message(f"Starting parsing of XML from {input_xml_path}...")
    df = parse_masters_xml(input_xml_path)
    
    log_message("[INFO] First 5 rows of the parsed DataFrame:")
    print(df.head())
    log_message("[INFO] Last 5 rows of the parsed DataFrame:")
    print(df.tail())

    log_message(f"Saving CSV to {output_csv_path}...")
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    log_message(f"Saved CSV with {len(df):,} rows.")
    
if __name__ == '__main__':
    main()
