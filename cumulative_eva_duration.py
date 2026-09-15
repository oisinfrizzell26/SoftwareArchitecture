import json
from datetime import datetime
import matplotlib.pyplot as plt

with open("eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)

selected_country = input("Enter a country: ")

records = []
country_total_hours = 0

for eva in eva_data:
    date_text = eva.get("date")
    duration_text = eva.get("duration")

    if not date_text or not duration_text:
        continue

    date = datetime.fromisoformat(date_text)
    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60

    if eva.get("country") == selected_country:
        country_total_hours += duration_hours

    records.append((date, duration_hours))

print(f"Total EVA duration for {selected_country}: {country_total_hours:.2f} hours")

records.sort(key=lambda record: record[0])

dates = []
cumulative_hours = []
total_hours = 0

for date, duration_hours in records:
    total_hours += duration_hours
    dates.append(date)
    cumulative_hours.append(total_hours)

plt.plot(dates, cumulative_hours)
plt.xlabel("Year")
plt.ylabel("Cumulative EVA duration (hours)")
plt.tight_layout()
plt.savefig("cumulative_duration.png")

annual_hours = {}
for date, duration_hours in records:
    annual_hours[date.year] = annual_hours.get(date.year, 0) + duration_hours

years = sorted(annual_hours)
totals = [annual_hours[year] for year in years]

plt.figure()
plt.bar(years, totals)
plt.xlabel("Year")
plt.ylabel("Annual EVA duration (hours)")
plt.tight_layout()
plt.savefig("annual_duration.png")

plt.show()
