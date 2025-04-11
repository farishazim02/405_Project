import os
import xml.etree.ElementTree as ET
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv

# List of XML files to process (adjust as needed)
FILES_TO_PROCESS = [
    "rel_chunk_1.xml",
    "rel_chunk_4.xml",
    "rel_chunk_5.xml",
    "rel_chunk_6.xml"
]

# Log file name
LOG_FILE = "extract_csv_log.txt"
# Print progress every 100K releases processed
CHECKPOINT_INTERVAL = 100000

def get_timestamp():
    """Return current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_message(message):
    """Prints a message with a timestamp to both the console and the log file."""
    ts = get_timestamp()
    full_msg = f"[{ts}] {message}"
    print(full_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

def extract_release(elem):
    """
    Extract required fields from a <release> element.
    Returns a list: [id, title, country, released, status, artist].
    If a critical field (e.g. id) is missing, returns None.
    """
    try:
        rel_id = elem.attrib.get("id", "").strip()
        if not rel_id:
            log_message("⚠️ Skipping release due to missing id.")
            return None
        status = elem.attrib.get("status", "").strip()
        title = (elem.findtext("title") or "").strip()
        country = (elem.findtext("country") or "").strip()
        released = (elem.findtext("released") or "").strip()
        artist_node = elem.find("artists/artist/name")
        artist = artist_node.text.strip() if artist_node is not None and artist_node.text else ""
        return [rel_id, title, country, released, status, artist]
    except Exception as e:
        log_message(f"❌ Error extracting release: {e}")
        return None

def process_xml_file(xml_file, limit=None):
    """
    Processes the XML file:
      - Iteratively parses the file and extracts each <release> element.
      - For each release, extracts: id, title, country, released, status, artist.
      - If extraction fails for a release, that release is skipped.
      - Logs progress every CHECKPOINT_INTERVAL releases.
      - If limit is provided (not None), stops after that many releases.
      - Saves all extracted records to a CSV file named "releases_part_{xmlfilename}.csv".
    Returns a tuple (xml_file, records).
    """
    base_name = os.path.basename(xml_file)
    output_csv = f"releases_part_{os.path.splitext(base_name)[0]}.csv"
    log_message(f"🚀 Started processing {xml_file} → {output_csv} (processing full file)")
    
    records = []
    count = 0
    try:
        context = ET.iterparse(xml_file, events=("end",))
        _, root = next(context)
    except Exception as e:
        log_message(f"❌ Error initializing iterparse on {xml_file}: {e}")
        return xml_file, records

    for event, elem in context:
        if elem.tag == "release":
            rec = extract_release(elem)
            if rec is not None:
                records.append(rec)
            count += 1

            if count % CHECKPOINT_INTERVAL == 0:
                last_id = rec[0] if rec else "N/A"
                log_message(f"✅ {xml_file}: Processed {count:,} releases; last release id: {last_id}")
            if limit is not None and count >= limit:
                log_message(f"✅ {xml_file}: Reached processing limit of {limit} releases; stopping extraction.")
                break

            elem.clear()
            root.clear()

    log_message(f"🎯 Finished processing {xml_file}: extracted {len(records):,} valid releases (total processed: {count:,}).")
    
    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id", "title", "country", "released", "status", "artist"])
            writer.writerows(records)
        log_message(f"📁 Saved CSV to {output_csv} with {len(records):,} rows.")
    except Exception as e:
        log_message(f"❌ Error writing CSV for {xml_file}: {e}")
    
    return xml_file, records

def main():
    log_message("=== 🚦 Starting parallel extraction for FULL dataset ===")
    results = {}
    
    # Process each XML file in parallel; set limit=None to process the full file
    with ProcessPoolExecutor(max_workers=len(FILES_TO_PROCESS)) as executor:
        futures = {
            executor.submit(process_xml_file, xml_file, limit=None): xml_file
            for xml_file in FILES_TO_PROCESS
        }
        for future in as_completed(futures):
            xml_file = futures[future]
            try:
                file_name, recs = future.result()
                results[xml_file] = recs
                log_message(f"✅ Completed processing {xml_file}: extracted {len(recs):,} releases.")
            except Exception as e:
                log_message(f"❌ Error processing {xml_file}: {e}")
    
    total = sum(len(recs) for recs in results.values())
    log_message("=== 🚦 Extraction complete. Summary: ===")
    for xml_file, recs in results.items():
        log_message(f"{xml_file}: {len(recs):,} rows extracted.")
    log_message(f"🧮 Total records processed across all files: {total:,}")

if __name__ == "__main__":
    main()
