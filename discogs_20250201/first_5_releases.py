import xml.etree.ElementTree as ET

file_path = "discogs_20250201_releases.xml"
context = ET.iterparse(file_path, events=("end",))
count = 0
seen = 0

for event, elem in context:
    if elem.tag == "release":
        seen += 1

        release_id = elem.attrib.get("id")
        title = elem.findtext("title")
        country = elem.findtext("country")
        released = elem.findtext("released")
        status = elem.attrib.get("status")

        artist_name = None
        artist_node = elem.find("artists/artist/name")
        if artist_node is not None:
            artist_name = artist_node.text

        # 🧠 Only print non-empty releases
        if any([title, country, released, artist_name]):
            print("➡️ Raw XML:")
            print(ET.tostring(elem, encoding='unicode')[:300])
            print()

            print(f"🆔 ID: {release_id}")
            print(f"🎵 Title: {title}")
            print(f"🌍 Country: {country}")
            print(f"📅 Released: {released}")
            print(f"📦 Status: {status}")
            print(f"🎤 Artist: {artist_name if artist_name else 'N/A'}")
            print("-" * 60)

            count += 1
        else:
            print(f"⏭️ Skipping empty release #{seen} (ID={release_id})")

        if count >= 5:
            break
        elem.clear()
