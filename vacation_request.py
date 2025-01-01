import argparse
import json
import fitz  # PyMuPDF
import csv
from datetime import datetime
import os

def add_text_to_pdf(input_pdf, output_pdf, text_positions, texts):
    """
    Add text to a PDF file at specified positions.

    :param input_pdf: Path to the input PDF file
    :param output_pdf: Path to the output PDF file
    :param text_positions: List of dictionaries with x, y coordinates
    :param texts: List of text strings to be added
    """
    # Open the input PDF
    pdf_document = fitz.open(input_pdf)

    # Iterate over all pages
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # Add text to the specified positions
        for idx, position in enumerate(text_positions):
            if idx < len(texts):
                x = position.get("x", 0)
                y = position.get("y", 0)
                text = texts[idx]
                # Add text to the page
                page.insert_text((x, y), text, fontsize=12, color=(0, 0, 0))

    # Save the output PDF
    pdf_document.save(output_pdf)
    print(f"Text added to '{output_pdf}' successfully.")

def write_text_to_csv(texts, year):
    """
    Write the provided texts to a CSV file named based on the year in the last text (assumed to be a date).

    :param texts: List of text strings to write to the CSV
    """
    csv_filename = f"{year}/{year}.csv"

    # Get the current datetime
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Headers for the CSV
    if len(texts) == 5:
        headers = ["from", "to", "days", "sign_date", "sign_location", "datetime"]
    else:
        headers = ["from", "to", "days", "sign_date", "datetime"]

    # Write to CSV
    file_exists = False
    try:
        file_exists = open(csv_filename, "r").close() is None
    except FileNotFoundError:
        pass

    with open(csv_filename, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(headers)  # Write the header only if the file does not exist
        writer.writerow(texts + [current_datetime])  # Write the data row

    print(f"Text data written to '{csv_filename}' successfully.")


def generate_output_filename(config, texts, year):
    """
    Generate the default output file name based on config and text inputs.

    :param config: Configuration dictionary from the JSON file
    :param texts: List of text inputs (including start date and days)
    :return: Generated file name as a string
    """
    prefix = config.get("Prefix", "Prefix")
    family_name = config.get("FamilyName", "FamilyName")
    start_date = texts[0]  # Assuming the start date is the first text
    days = texts[2]  # Assuming the total days are the third text

    filename = f"{year}/{prefix}_{start_date}_{days}d_{family_name}.pdf"
    return filename


def main():
    parser = argparse.ArgumentParser(description="Add text to a PDF at specified positions.")
    parser.add_argument("pdf", type=str, help="Path to the input PDF file")
    parser.add_argument("config", type=str, help="Path to the configuration JSON file")
    #parser.add_argument("output", type=str, help="Path to the output PDF file")
    parser.add_argument("texts", nargs='+', type=str, help="List of text strings to be added: from, to, days, sign_date, (sign_location)")

    args = parser.parse_args()

    # Check dates
    from_date = args.texts[0]  # Assuming the date is the last text input
    to_date = args.texts[1]  # Assuming the date is the last text input
    sign_date = args.texts[3]  # Assuming the date is the last text input
    for date in [sign_date, to_date, from_date]:
        try:
            year = str(datetime.strptime(date, "%d.%m.%Y").year)
        except ValueError:
            print("Error: The date input is not a valid date in DD.MM.YYYY format.")
            return

    # Create folder     
    if not os.path.exists(year):
        os.makedirs(year)

    # Load configuration JSON
    with open(args.config, "r") as config_file:
        config = json.load(config_file)

    text_positions = config.get("text_positions", [])
    if not text_positions:
        print("Error: No text positions found in the config file.")
        return

    if len(args.texts) != len(text_positions):
        print("Error: Number of texts does not match the number of text positions.")
        return

    # Generate default output file name
    output_filename = generate_output_filename(config, args.texts, year)


    # Add text to the PDF
    add_text_to_pdf(args.pdf, output_filename, text_positions, args.texts)

    # Write text data to a CSV file
    write_text_to_csv(args.texts, year)

if __name__ == "__main__":
    main()
