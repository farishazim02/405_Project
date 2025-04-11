import xml.etree.ElementTree as ET
import pandas as pd
import time

file_path = "discogs_20250201_artists.xml"
start = time.time()

print("🚀 Extracting all non-empty <artist> records...")

context = ET.iterparse(file_path, events=("end",))
rows = []
count = 0
seen = 0

for event, elem in context:
    if elem.tag == "artist":
        seen += 1

        artist_id = elem.findtext("id")
        name = elem.findtext("name")
        realname = elem.findtext("realname")
        profile = elem.findtext("profile")

        if any([artist_id, name, realname, profile]):
            rows.append({
                "id": artist_id,
                "name": name,
                "realname": realname,
                "profile": profile
            })
            count += 1

        if seen % 50000 == 0:
            print(f"🔄 Seen: {seen} artists, Collected: {count}")
        elem.clear()

# ✅ PREVIEW: raw extracted rows before DataFrame
print("\n🔍 First 5 rows (raw dicts):")
for r in rows[:5]:
    print(r)

print("\n🔍 Last 5 rows (raw dicts):")
for r in rows[-5:]:
    print(r)

# ✅ Create DataFrame after preview
df = pd.DataFrame(rows)

# Save
df.to_csv("artists_full.csv", index=False)
print(f"\n✅ Saved artists_full.csv with {len(df)} rows")

end = time.time()
print(f"⏱ Total time: {round(end - start, 2)} seconds")
