import fastf1
fastf1.Cache.enable_cache('./cache')
import csv

# Event Info
with open('event_info.csv', 'w', newline='') as event_file:
    writer = csv.writer(event_file)
    writer.writerow(["Year", "Name", "Country", "Location", "Laps"])
    for i in range(6):
        year = 2018 + i
        events = fastf1.get_event_schedule(year)
        for j in range(len(events)):
            race_name = events.iloc[j].EventName
            country = events.iloc[j].Country
            race_location = events.iloc[j].Location
            race = fastf1.get_session(year, race_name, 'R')
            race.load()
            race_laps = race.laps['LapNumber'].max()
            writer.writerow([year, race_name, country, race_location, race_laps])
            
# Race Conditions
with open('weather_data.csv', 'w', newline='') as weather_file:
    writer = csv.writer(weather_file)
    writer.writerow(["Year", "Name", "Temperature", "Humidity", "Pressure", "Wind"])
    for i in range(6):
        year = 2018 + i
        events = fastf1.get_event_schedule(year)
        for j in range(len(events)):
            race_name = events.iloc[j].EventName
            race = fastf1.get_session(year, race_name, 'R')
            race.load()
            weather = race.weather_data[:1]
            temp = weather['AirTemp'].values[0]
            humidity = weather['Humidity'].values[0]
            pressure = weather['Pressure'].values[0]
            wind = weather['WindSpeed'].values[0]
            writer.writerow([year,race_name,temp,humidity,pressure,wind])

# # Tire Strategy Data
with open('tire-strategy.csv', 'w', newline='') as tire_file:
    writer = csv.writer(tire_file)
    writer.writerow(["Year", "Race", "Driver", "Stint", "Compound", "StintLength"])
    for i in range(6):
        year = 2018 + i
        events = fastf1.get_event_schedule(year)
        for j in range(len(events)):
            race_name = events.iloc[j].EventName
            race = fastf1.get_session(year, race_name, 'R')
            race.load()
            laps = race.load_laps(with_telemetry=True)
            driver_stints = laps[['Driver', 'Stint', 'Compound', 'LapNumber']].groupby(['Driver', 'Stint', 'Compound']).count().reset_index()
            driver_stints = driver_stints.rename(columns={'LapNumber': 'StintLength'})
            driver_stints = driver_stints.sort_values(by=['Stint'])
            for k in range(len(driver_stints)):
                driver = driver_stints.iloc[k].Driver
                stint = driver_stints.iloc[k].Stint
                compound = driver_stints.iloc[k].Compound
                stint_length = driver_stints.iloc[k].StintLength
                writer.writerow([year, race_name, driver, stint, compound, stint_length])
