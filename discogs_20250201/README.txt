README: discogs_20250201 folder

This folder contains scripts and data extracted from the Discogs XML files.

1. After unzipping the XML files, my recommendation is to start by testing/extracting the first 5 lines from each XML file. This will give you a quick understanding of the structure of the data. For this, I created test scripts for each of the XML files.

2. The `artists.xml` and `masters.xml` files were directly extracted to CSV since their sizes were moderate and manageable.

3. The large `releases.xml` file (~56 GB) was first split into 6 smaller chunks: `rel_chunk_1.xml` to `rel_chunk_6.xml`.

4. I processed the chunks in parallel to extract them to CSV. However, chunks 1 and 6 had structural issues (some interrupted XML parts), so I used a separate script for those two to skip the corrupted parts during extraction.

5. I also included a test script to check for missing values in the resulting CSV files, just to double-check the integrity of the extracted data.

6. I first uploaded all relevant Python scripts and then uploaded the CSV files (those under GitHub’s 100MB file size limit).

Let me know if you have questions!
