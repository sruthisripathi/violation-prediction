import json
from random import randrange

class Data:

    data_tree = None
    place_tree = None
    drivers = None
    NO_VALUE_GIVEN = "-"
    patterns = [
        "place has n times the average no of violations",
        "service provider has n times the average violations",
        "service provider in a terminal has n times the average violations",
        "driver has n times the average violations",
        "driver forgets to change status",
        "driver has more probability of violation at certain time of day",
        "driver has more probability of violation on a certain weekday",
        "driver has more probability of violation at a certain time of month",
        "holiday",
        "place has "
    ]

    def no_value(self, val):
        return val == self.NO_VALUE_GIVEN

    def get_place_tree_from_user(self):
        no_of_regions = int(input("No of regions: "))
        for i in range(no_of_regions):
            region_name = input("Name of the region: ")
            if self.no_value(region_name):
                region_name = f"r{i+1}"
            self.place_tree[region_name] = dict({})
            path_till_now = f"{region_name}>"
            no_of_districts = int(input(f"No of districts in {path_till_now} region: "))
            for j in range(no_of_districts):
                region_name = input(f"Name of the District ({path_till_now}): ")
                if self.no_value(region_name):
                    district_name = f"{region_name}_d{j+1}"
                self.place_tree[region_name][district_name] = dict({})
                path_till_now = f"{region_name}>{district_name}>"
                no_of_stations = int(input(f"No of stations in {path_till_now} district: "))
                for k in range(no_of_stations):
                    path_till_now = f"{region_name}>"
                    region_name = input(f"Name of the District ({path_till_now}): ")
                    if self.no_value(region_name):
                        station_name = f"{district_name}_s{k+1}"
                    self.place_tree[region_name][district_name][station_name] = list()
                    path_till_now = f"{region_name}>{district_name}>{station_name}>"
                    no_of_terminals = int(input(f"No of terminals {path_till_now} station: "))
                    for l in range(no_of_terminals):
                        terminal_name = f"{station_name}_t{l+1}"
                        self.place_tree[region_name][district_name][station_name].append(terminal_name)
                        # no_of_drivers = int(input(f"No of drivers in {terminal_name} terminal: "))
                        # places[region_name][district_name][station_name][terminal_name] = no_of_drivers

    def get_data_from_json_file(self, data_key, file_name):
        with open(file_name) as json_file:
            self[data_key] = json.load(json_file)

    def flatten_place_tree_into_list(self):
        records = list()
        for region, districts in self.place_tree:
            for district, stations in districts:
                for station, terminals in stations:
                    for terminal in terminals:
                        records.append({
                            "region": region,
                            "district": district,
                            "station": station,
                            "terminal": terminal
                        })
    
    def flatten_place_tree_into_dict(self):
        records = dict({})
        for region, districts in self.place_tree:
            for district, stations in districts:
                for station, terminals in stations:
                    for terminal in terminals:
                        records[terminal]['place_hierarchy'] = {
                            "region": region,
                            "district": district,
                            "station": station
                        }

    def get_service_provicers_from_user(self):
        """Get service providers"""

    def get_drivers_from_user(self):
        all_terminals = self.flatten_place_tree_into_dict()
        for terminal in all_terminals:
            ph = terminal['place_hierarchy'] 
            ph_str = f"{ph['region']}>{ph['district']}>{ph['station']}>{terminal}"
            no_of_drivers = int(input(f"No of drivers in {ph_str} terminal: "))
            for i in range(no_of_drivers):
                self.drivers[ph_str].append(f"{terminal}_driver_{i+1}")

    def get_patterns_from_user(self):
        """Gets patterns: how or HOW, I DON'T KNOW YET"""

# driver_counts = []
# for i in range(15):
#     driver_counts.append(randrange(3)+1)

# print(driver_counts)

# driver_counts = [1, 3, 3, 1, 1, 3, 2, 1, 2, 1, 2, 1, 1, 3, 1]
# print(sum(driver_counts))

# no_of_terminals = 15
# teminal_patterns = {

# }
    
# for i in range(no_of_terminals):
#     teminal_patterns[f"terminal_{i+1}"] = {}

# print(teminal_patterns)

# terminal_patterns = {
#     "terminal_1": {
#         "n_times"
#     },
#     "terminal_2": {},
#     "terminal_3": {},
#     "terminal_4": {},
#     "terminal_5": {},
#     "terminal_6": {},
#     "terminal_7": {},
#     "terminal_8": {},
#     "terminal_9": {},
#     "terminal_10": {},
#     "terminal_11": {},
#     "terminal_12": {},
#     "terminal_13": {},
#     "terminal_14": {},
#     "terminal_15": {}
# }

total_violations = 4173

regions = {}

with open("place_patterns_v0.json") as json_file:
    regions = json.load(json_file)

# print(regions)

place_total_violations = {}

# print(regions["region_1"])
# print(list(regions.keys()))
place_violations_table = []

for region_name, region in regions.items():
    region_total_violations = round(region["patterns"]["total_percentage"] * total_violations)
    place_violations_table.append({
        "place_id": region_name,
        "place_type": "region",
        "total_violations": region_total_violations
    })
    place_total_violations[region_name] = {
        "total_violations": region_total_violations,
        "districts": {}
    }
    districts = region["districts"]
    for district_name, district in districts.items():
        district_total_violations = round(district["patterns"]["total_percentage"] * region_total_violations)
        place_violations_table.append({
            "place_id": district_name,
            "place_type": "district",
            "total_violations": district_total_violations
        })
        place_total_violations[region_name]["districts"][district_name] = {
            "total_violations": district_total_violations,
            "stations": {}
        }
        stations = district["stations"]
        for station_name, station in stations.items():
            station_total_violations = round(station["patterns"]["total_percentage"] * district_total_violations)
            place_violations_table.append({
                "place_id": station_name,
                "place_type": "station",
                "total_violations": station_total_violations
            })
            place_total_violations[region_name]["districts"][district_name]["stations"][station_name] = {
                "total_violations": station_total_violations,
                "terminals": {}
            }
            terminals = station["terminals"]
            for terminal_name, terminal in terminals.items():
                terminal_total_violations = round(terminal["patterns"]["total_percentage"] * station_total_violations)
                place_violations_table.append({
                    "place_id": terminal_name,
                    "place_type": "terminal",
                    "total_violations": terminal_total_violations
                })
                place_total_violations[region_name]["districts"][district_name]["stations"][station_name]["terminals"][terminal_name] = {
                    "total_violations": terminal_total_violations,
                }
            
print(place_violations_table)