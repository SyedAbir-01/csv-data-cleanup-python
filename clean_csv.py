import argparse
import csv
import os
import sys
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Clean CSV files by removing blank rows, normalizing whitespace, "
                    "and removing duplicate records."
    )

    parser.add_argument(
        "input",
        help="Path to the input CSV file"
    )

    parser.add_argument(
        "output",
        help="Path where the cleaned CSV file will be saved"
    )

    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Convert text values to lowercase"
    )

    parser.add_argument(
        "--report",
        default=None,
        help="Optional path for the cleaning report"
    )

    return parser.parse_args()


def clean_text(value, lowercase=False):
    """Remove unnecessary whitespace and optionally convert text to lowercase."""
    cleaned = value.strip()

    if lowercase:
        cleaned = cleaned.lower()

    return cleaned


def is_empty_row(row):
    """Return True when every cell in the row is empty."""
    return all(cell == "" for cell in row)


def generate_report(
    input_file,
    output_file,
    rows_processed,
    empty_rows_removed,
    duplicates_removed,
    rows_exported,
    lowercase
):
    """Create a human-readable cleaning report."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = [
        "CSV CLEANING REPORT",
        "=" * 40,
        f"Completed: {timestamp}",
        "",
        f"Input file:            {input_file}",
        f"Output file:           {output_file}",
        "",
        f"Rows processed:        {rows_processed}",
        f"Empty rows removed:    {empty_rows_removed}",
        f"Duplicates removed:    {duplicates_removed}",
        f"Rows exported:         {rows_exported}",
        "",
        "Cleaning performed:",
        "✓ Whitespace normalized",
        "✓ Empty rows removed",
        "✓ Duplicate rows removed",
        f"✓ Lowercase conversion: {'Enabled' if lowercase else 'Disabled'}",
    ]

    return "\n".join(report)


def clean_csv(input_file, output_file, report_file=None, lowercase=False):
    """Clean the input CSV and save the cleaned result."""

    if not os.path.isfile(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    if os.path.abspath(input_file) == os.path.abspath(output_file):
        print("Error: Input and output files must be different.")
        sys.exit(1)

    seen = set()
    cleaned_rows = []

    rows_processed = 0
    empty_rows_removed = 0
    duplicates_removed = 0

    try:
        with open(
            input_file,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as infile:

            reader = csv.reader(infile)

            try:
                header = next(reader)
            except StopIteration:
                print("Error: The input CSV file is empty.")
                sys.exit(1)

            # Clean the header's whitespace but preserve capitalization.
            header = [cell.strip() for cell in header]
            cleaned_rows.append(header)

            for row in reader:
                rows_processed += 1

                cleaned_row = [
                    clean_text(cell, lowercase)
                    for cell in row
                ]

                # Remove rows where every cell is empty.
                if is_empty_row(cleaned_row):
                    empty_rows_removed += 1
                    continue

                row_tuple = tuple(cleaned_row)

                # Remove duplicate records.
                if row_tuple in seen:
                    duplicates_removed += 1
                    continue

                seen.add(row_tuple)
                cleaned_rows.append(cleaned_row)

        output_directory = os.path.dirname(os.path.abspath(output_file))

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as outfile:

            writer = csv.writer(outfile)
            writer.writerows(cleaned_rows)

    except PermissionError:
        print(
            "Error: Permission denied. "
            "Make sure the file is not open in another program."
        )
        sys.exit(1)

    except csv.Error as error:
        print(f"Error: Could not process CSV file: {error}")
        sys.exit(1)

    except OSError as error:
        print(f"Error: File operation failed: {error}")
        sys.exit(1)

    rows_exported = len(cleaned_rows) - 1

    report = generate_report(
        input_file=input_file,
        output_file=output_file,
        rows_processed=rows_processed,
        empty_rows_removed=empty_rows_removed,
        duplicates_removed=duplicates_removed,
        rows_exported=rows_exported,
        lowercase=lowercase
    )

    print()
    print(report)

    if report_file:
        try:
            report_directory = os.path.dirname(
                os.path.abspath(report_file)
            )

            if not os.path.exists(report_directory):
                os.makedirs(report_directory)

            with open(
                report_file,
                "w",
                encoding="utf-8"
            ) as report_output:
                report_output.write(report)

            print()
            print(f"Report saved to: {report_file}")

        except OSError as error:
            print(f"Warning: Could not save report: {error}")


def main():
    args = parse_arguments()

    clean_csv(
        input_file=args.input,
        output_file=args.output,
        report_file=args.report,
        lowercase=args.lowercase
    )


if __name__ == "__main__":
    main()
