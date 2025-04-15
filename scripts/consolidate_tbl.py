#!/usr/bin/env python3
import os
import glob
import csv
import sys

# Define the expected header
HEADER = [
    "target name", "accession", "query name", "accession",
    "E-value", "score", "bias", "E-value", "score", "bias",
    "exp", "reg", "clu", "ov", "env", "dom", "rep", "inc", "description of target"
]

def parse_tbl_file(filepath):
    """
    Parses a _results.tbl file.
    It skips commented lines and blank lines.
    Each result row is split using maxsplit=19 so that we obtain 20 fields.
    Returns a list of rows (each row is a list of 20 columns).
    """
    rows = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            # Skip comment lines (starting with '#') and blank lines.
            if not line or line.startswith("#"):
                continue
            # Split the line into 20 fields so that the last field captures the full description.
            parts = line.split(None, 18)
            if len(parts) < 19:
                # If the row doesn't have enough columns, skip it.
                continue
            rows.append(parts)
    return rows

def main(directory="."):
    os.chdir(directory)
    # Find all files ending with _results.tbl in the directory.
    tbl_files = glob.glob("*_results.tbl")
    if not tbl_files:
        print("No _results.tbl files found in the directory.")
        return

    consolidated_rows = []
    
    # Process each _results.tbl file.
    for tbl_file in tbl_files:
        rows = parse_tbl_file(tbl_file)
        # If you want to include the source file column, append it to each row.
        for row in rows:
            consolidated_rows.append(row + [tbl_file])

    if not consolidated_rows:
        print("No valid result rows found in any _results.tbl file.")
        return

    # Define the CSV header: our fixed header plus a "source_file" column.
    csv_header = HEADER + ["source_file"]

    # Write out the consolidated CSV file.
    output_csv = "consolidated_results.csv"
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        writer.writerows(consolidated_rows)

    print(f"Consolidated CSV file created: {output_csv}")

if __name__ == "__main__":
    # Optionally pass the directory as the first command-line argument.
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    main(target_dir)

