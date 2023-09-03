from sys import argv
from datetime import datetime
import json

def convert_date(date_str):
    # Split the string by " – " to separate the date part from the time part
    date_parts = date_str.split(" – ")

    # Extract the date and time parts
    date_part = date_parts[0]
    time_part = date_parts[1].rstrip(" UTC")

    # Define a dictionary to map month names to their numerical representation
    month_dict = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    # Split the date part into day, month, and year
    day, month_name, year = date_part.split()
    month = month_dict[month_name]
    year = int(year)

    # Split the time part into hours, minutes, and seconds
    hours, minutes, seconds = map(int, time_part.split(':'))

    # Create a datetime object
    parsed_date = datetime(year, month, int(day), hours, minutes, seconds)

    return parsed_date

if not argv[1].endswith(".tsv"):
    exit(0)

f = open(argv[1], 'r', encoding='utf8')
out = argv[1].replace('tsv', 'json')
print(out)

manifests = []
for l in f.readlines():
    l = l.rstrip("\n").split("\t")
    date = l[0]
    manifest = l[2]
    date_iso = f"{convert_date(date).isoformat('T')}Z"
    manifests.append({
        "date": date_iso,
        "id": manifest
    })

open(out, 'w').write(json.dumps(manifests, indent=True))
