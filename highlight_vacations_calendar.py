import argparse
import pandas as pd
import calendar
from datetime import datetime
import matplotlib.pyplot as plt


def read_legal_holidays(file_path):
    """
    Read legal holidays from a CSV file.

    :param file_path: Path to the CSV file
    :return: Set of dates (dd.mm.YYYY) for legal holidays
    """
    try:
        holidays_df = pd.read_csv(file_path, parse_dates=["date"], dayfirst=True)
        return set(holidays_df["date"].dt.strftime("%d.%m.%Y"))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return set()

def read_taken_vacations(year):
    """
    Read taken vacations from the CSV file for the given year.

    :param year: Year for which to read taken vacations
    :return: Set of dates (dd.mm.YYYY) for taken vacations
    """
    csv_filename = f"{year}/{year}.csv"
    taken_vacations = set()

    try:
        vacations_df = pd.read_csv(csv_filename)
        for _, row in vacations_df.iterrows():
            start_date = datetime.strptime(row["from"], "%d.%m.%Y")
            end_date = datetime.strptime(row["to"], "%d.%m.%Y")
            current_date = start_date
            while current_date <= end_date:
                taken_vacations.add(current_date.strftime("%d.%m.%Y"))
                current_date += pd.Timedelta(days=1)
    except FileNotFoundError:
        print(f"No taken vacations found for year {year}. Assuming none.")
    except Exception as e:
        print(f"Error reading taken vacations: {e}")

    return taken_vacations


def read_school_vacations(file_path):
    """
    Read school vacations from a CSV file.

    :param file_path: Path to the CSV file
    :return: Set of dates (dd.mm.YYYY) for school vacations
    """
    try:
        vacations_df = pd.read_csv(file_path, parse_dates=["start", "end"], dayfirst=True)
        school_vacations = set()
        for _, row in vacations_df.iterrows():
            start_date = row["start"]
            end_date = row["end"]
            current_date = start_date
            while current_date <= end_date:
                school_vacations.add(current_date.strftime("%d.%m.%Y"))
                current_date += pd.Timedelta(days=1)
        return school_vacations
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return set()


def create_calendar(year, taken_vacations, legal_holidays, school_vacations):
    """
    Create a calendar for the given year with highlighted vacations.

    :param year: Year to create the calendar for
    :param taken_vacations: Set of taken vacation dates
    :param legal_holidays: Set of state vacation dates
    :param school_vacations: Set of school vacation dates
    """
    cal = calendar.Calendar()

    plt.figure(figsize=(16, 12))
    plt.suptitle(f"Calendar for {year}", fontsize=20)

    for month in range(1, 13):
        ax = plt.subplot(4, 3, month)
        ax.set_title(calendar.month_name[month], fontsize=16)
        ax.axis("off")

        month_days = cal.monthdayscalendar(year, month)
        dates = []

        for week in month_days:
            dates.append([
                (f"{day:02d}.{month:02d}.{year}" if day != 0 else "") for day in week
            ])


        table_data = []
        cell_colors = []
        week_fonts = []  # To define font weight (bold or normal)

        for week_idx, week in enumerate(dates):
            week_colors = []
            week_row_fonts = []  # To define font weight (bold or normal)
            for day_idx, date in enumerate(week):
                if day_idx in [5, 6] and date:  # Saturdays and Sundays
                    week_colors.append("#ffcccc")  # Light Red for weekends
                elif date in legal_holidays:
                    week_colors.append("#cd1c18")  # Red for state vacations
                elif date in taken_vacations:
                    week_colors.append("#cce5ff")  # Light blue for taken vacations
                elif date in school_vacations:
                    #week_colors.append("#ffffff")  # White for regular days
                    week_colors.append("#ffffcc")  # Light yellow for school vacations
                else:
                    week_colors.append("#ffffff")  # White for regular days

            for day_idx, date in enumerate(week):
                if day_idx in [5, 6] and date:  # Saturdays and Sundays
                    week_row_fonts.append("normal")
                elif date in legal_holidays:
                    week_row_fonts.append("normal")
                elif date in taken_vacations:
                    week_row_fonts.append("normal")
                elif date in school_vacations:
                    week_row_fonts.append("bold")
                else:
                    week_row_fonts.append("normal")

            table_data.append(week)
            cell_colors.append(week_colors)
            week_fonts.append(week_row_fonts)

        table = ax.table(
            cellText=[[
                (f"$\\bf{day}$" if font == "bold" else day) if day != "" else ""
                for day, font in zip(week, fonts)
            ] for week, fonts in zip(table_data, week_fonts)],
            cellColours=cell_colors,
            cellLoc="center",
            loc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Generate a calendar with highlighted vacations.")
    parser.add_argument("year", type=int, help="Year for which to generate the calendar")
    parser.add_argument("legal_holidays_csv", type=str,  nargs='?', default="data/legal_holidays.csv", help="Path to the CSV file containing legal holidays")
    parser.add_argument("state_school_vacations_csv", type=str,  nargs='?', default="data/school_vacations.csv", help="Path to the CSV file containing school vacations")

    args = parser.parse_args()

    year = args.year
    legal_holidays = read_legal_holidays(args.legal_holidays_csv)
    school_vacations = read_school_vacations(args.state_school_vacations_csv)
    taken_vacations = read_taken_vacations(year)
    create_calendar(year, taken_vacations, legal_holidays, school_vacations)

if __name__ == "__main__":
    main()

