from load_map import load_map
from load_data import load_protagonist

# Загрузка карты
locations, start_location = load_map()


# for name, location in locations.items():
#     print(f"Location name: {name}")
#     print(f"Description: {location.description}")
#     print(f"Directions: {location.directions}")
#     print()  # Печатает пустую строку для разделения локаций


# Инициализация главного героя
protagonist = load_protagonist(start_location)


def main():
    print('Start walking test!')
    # print(protagonist.current_location.name)
    protagonist.whereami()
    print()
    # Cyber Street
    protagonist.go('north')
    print()
    # Back Alley
    protagonist.go('east')
    print()
    # Cyber Street
    protagonist.go('west')
    print()
    # Tech Market
    protagonist.go('north')
    print()
    # Hackers Den
    protagonist.go('west')


if __name__ == "__main__":
    main()
