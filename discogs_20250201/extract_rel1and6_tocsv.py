import os
from lxml import etree  # Using lxml (be sure to install it)
from datetime import datetime
import csv

# Global constants
LOG_FILE = "extract_csv_log6.txt"
CHECKPOINT_INTERVAL = 100000  # Log progress every 100K releases

def get_timestamp():
    """Return current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_message(message):
    """Print a message with timestamp and append it to the log file."""
    ts = get_timestamp()
    full_message = f"[{ts}] {message}"
    print(full_message)
    with open(LOG_FILE, "a", encoding="utf-8") as lf:
        lf.write(full_message + "\n")

def extract_release(elem):
    """
    Extract required fields from a <release> element.
    Returns a list: [id, title, country, released, status, artist] or None if a critical field is missing.
    """
    try:
        rel_id = elem.get("id", "").strip()
        if not rel_id:
            log_message("⚠️ Skipping release due to missing id.")
            return None
        status = elem.get("status", "").strip()
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
    Processes the given XML file using lxml with recover enabled.
    For each <release> element, attempts to extract:
      id, title, country, released, status, artist.
    Malformed releases that cannot be processed are skipped.
    Logs progress every CHECKPOINT_INTERVAL releases.
    Saves the valid extracted records to a CSV file.
    Writes parser error messages to an error log file.
    Returns a tuple (xml_file, records).
    """
    base_name = os.path.basename(xml_file)
    csv_output = f"releases_part_{os.path.splitext(base_name)[0]}.csv"
    error_output_file = f"errors_{os.path.splitext(base_name)[0]}.txt"
    
    log_message(f"🚀 Started processing {xml_file} → {csv_output} (using lxml recover mode)")
    
    records = []
    count = 0

    # Use iterparse with recover=True. (Note: In some versions, recover=True is accepted directly.)
    try:
        # Pass recover=True as a keyword argument without a separate parser object.
        context = etree.iterparse(xml_file, events=("end",), recover=True)
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
                last_id = rec[0] if rec is not None else "N/A"
                log_message(f"✅ {xml_file}: Processed {count:,} releases; last release id: {last_id}")
            if limit is not None and count >= limit:
                log_message(f"✅ {xml_file}: Reached processing limit of {limit} releases; stopping extraction.")
                break
            elem.clear()
            root.clear()
    
    log_message(f"🎯 Finished processing {xml_file}: processed {count:,} releases; extracted {len(records):,} valid records.")

    # Write parser error log (if available) to error_output_file
    try:
        # Access parser error log if available
        error_log = context.parser.error_log if hasattr(context, 'parser') and context.parser.error_log else None
    except Exception as e:
        error_log = None

    with open(error_output_file, "w", encoding="utf-8") as ef:
        if error_log:
            ef.write("Parser errors:\n")
            for error in error_log:
                ef.write(f"Line {error.line}, Column {error.column}: {error.message}\n")
        else:
            ef.write("No parser errors detected.\n")
    log_message(f"📑 Parser error log saved to {error_output_file}")

    # Write output CSV
    try:
        with open(csv_output, "w", newline="", encoding="utf-8") as cf:
            writer = csv.writer(cf)
            writer.writerow(["id", "title", "country", "released", "status", "artist"])
            writer.writerows(records)
        log_message(f"📁 Saved CSV to {csv_output} with {len(records):,} rows.")
    except Exception as e:
        log_message(f"❌ Error writing CSV for {xml_file}: {e}")
    
    return xml_file, records

def main():
    # Process only rel_chunk_1.xml for now
    xml_file = "rel_chunk_6.xml"
    process_xml_file(xml_file, limit=None)

if __name__ == "__main__":
    main()
