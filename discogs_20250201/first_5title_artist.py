import xml.etree.ElementTree as ET

file_path = "discogs_20250201_artists.xml"

context = ET.iterparse(file_path, events=("end",))
count = 0
seen = 0

for event, elem in context:
    if elem.tag == "artist":
        seen += 1
        print(f"➡️ New artist element #{seen}")
        print(ET.tostring(elem, encoding='unicode')[:300])  # print raw XML (first 300 chars)

        artist_id = elem.findtext("id")
        name = elem.findtext("name")
        realname = elem.findtext("realname")
        profile = elem.findtext("profile")

        print(f"  - Parsed ID: {artist_id}")
        print(f"  - Parsed Name: {name}")
        print(f"  - Parsed Real Name: {realname}")
        print(f"  - Parsed Profile: {profile}")

        # Only print non-empty artists
        if any([artist_id, name, realname, profile]):
            print("✅ Artist has useful data! Displaying:")
            print(f"🆔 ID: {artist_id}")
            print(f"🎤 Name: {name}")
            print(f"👤 Real Name: {realname}")
            print(f"📄 Profile: {profile}")
            print("-" * 60)
            count += 1
        else:
            print("⛔ Skipping empty artist entry.")
            print("-" * 60)

        if count >= 5:
            break
        elem.clear()
