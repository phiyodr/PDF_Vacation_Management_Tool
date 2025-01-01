import argparse
import json
import csv
from datetime import datetime

def calculate_remaining_vacations(year, vacations_json):
    """
    Calculate the remaining vacations for a given year.

    :param year: The year to calculate remaining vacations for
    :param vacations_json: Path to the JSON file containing vacation data per year
    """
    # Load vacation data from JSON
    with open(vacations_json, "r") as json_file:
        vacations_data = json.load(json_file)

    # Get the vacation data for the specified year
    year_data = vacations_data.get(str(year), {})
    if not year_data:
        print(f"No vacation data available for the year {year}.")
        return

    # Calculate total vacations from previous year, this year, and special vacations
    total_vacations = (
        int(year_data.get("vacation_from_previous_year", 0)) +
        int(year_data.get("vacation_from_this_year", 0)) +
        int(year_data.get("special_vacation", 0))
    )

    # Open the corresponding CSV file for the year
    csv_filename = f"{year}/{year}.csv"
    taken_vacations = 0

    try:
        with open(csv_filename, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Sum up the values in the "days" column (if present)
                days = row.get("days")
                if days and days.isdigit():
                    taken_vacations += int(days)
    except FileNotFoundError:
        print(f"No data found for year {year}. Assuming no vacations have been taken.")

    # Calculate remaining vacations
    remaining_vacations = total_vacations - taken_vacations

    print(f"Year: {year}")
    print(f"Total vacation entitlement: {total_vacations:2}")
    print(f"Taken vacations:            {taken_vacations:2}")
    print(f"Remaining vacations:        {remaining_vacations:2}")

    return remaining_vacations

def main():
    parser = argparse.ArgumentParser(description="Calculate remaining vacations for a given year.")
    parser.add_argument("year", type=int, help="Year to calculate remaining vacations for")
    parser.add_argument("vacations_json", type=str, nargs='?', default="data/vacation_entitlement.json", help="Path to the JSON file containing vacation data per year")

    args = parser.parse_args()

    calculate_remaining_vacations(args.year, args.vacations_json)

if __name__ == "__main__":
    main()

