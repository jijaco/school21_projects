import json
from models import Location

def load_map():
    """
    Загружает данные карты из файла JSON и создает объекты Location.
    """
    with open('map_data.json', 'r') as f:
        data = json.load(f)

    locations = {}
    for loc_data in data['locations']:
        loc_name = loc_data['name']
        loc_description = loc_data['description']
        location = Location(loc_name, loc_description, {})
        locations[loc_name] = location

    for loc_data in data['locations']:
        loc_name = loc_data['name']
        location = locations[loc_name]
        for direction, dest_name in loc_data['directions'].items():
            if dest_name in locations:
                location.add_direction(direction, locations[dest_name])

    start_location_name = data.get('start_location', 'None')
    start_location = locations.get(start_location_name, None)

    return locations, start_location
