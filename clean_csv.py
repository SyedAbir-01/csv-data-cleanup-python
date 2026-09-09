import csv
import sys


if len(sys.argv) != 3:
    print("Usage: python clean_csv.py <input.csv> <output.csv>")
    sys.exit(1)

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]


def clean_text(text):
    return text.strip().lower()


def clean_csv():
    seen = set()
    cleaned_rows = []

    rows_processed = 0
    duplicates_removed = 0

    with open(INPUT_FILE, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        cleaned_rows.append(header)

        for row in reader:
            rows_processed += 1

            cleaned_row = [clean_text(cell) for cell in row]
            row_tuple = tuple(cleaned_row)

            if row_tuple not in seen:
                seen.add(row_tuple)
                cleaned_rows.append(cleaned_row)
            else:
                duplicates_removed += 1

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)

    print("\nCSV CLEANUP COMPLETE")
    print("--------------------")
    print(f"Rows processed: {rows_processed}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Rows exported: {len(cleaned_rows) - 1}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_csv()
