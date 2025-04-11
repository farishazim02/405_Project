import xml.etree.ElementTree as ET

context = ET.iterparse("discogs_20250201_masters.xml", events=("end",))
count = 0

for event, elem in context:
    if elem.tag == "master":
        print("➡️ New master element found")
        print(ET.tostring(elem, encoding="unicode")[:500])  # show first 500 chars of full element

        # Now extract
        title = elem.findtext("title")
        year = elem.findtext("year")
        genres = [g.text for g in elem.findall("genres/genre") if g.text]
        styles = [s.text for s in elem.findall("styles/style") if s.text]
        main_release_id = elem.findtext("main_release")

        artist_name = None
        artist_node = elem.find("artists/artist/name")
        if artist_node is not None:
            artist_name = artist_node.text

        print(f"🎵 ID: {elem.attrib.get('id')}")
        print(f"📀 Title: {title}")
        print(f"📅 Year: {year}")
        print(f"🔗 Main Release ID: {main_release_id}")
        print(f"🎼 Genre: {', '.join(genres)}")
        print(f"🎧 Style: {', '.join(styles)}")
        print(f"👤 Artist: {artist_name if artist_name else 'N/A'}")
        print("-" * 60)

        count += 1
        if count >= 5:
            break

        elem.clear()
