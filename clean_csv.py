import csv

INPUT_FILE = "input.csv"
OUTPUT_FILE = "output.csv"


def clean_text(text):
    return text.strip().lower()


def clean_csv():
    seen = set()
    cleaned_rows = []

    with open(INPUT_FILE, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        cleaned_rows.append(header)

        for row in reader:
            cleaned_row = [clean_text(cell) for cell in row]
            row_tuple = tuple(cleaned_row)

            if row_tuple not in seen:
                seen.add(row_tuple)
                cleaned_rows.append(cleaned_row)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)

    print("CSV cleaned successfully!")


if __name__ == "__main__":
    clean_csv()
