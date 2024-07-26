import random


def turrets_generator():
    personality_traits = ['neuroticism', 'openness',
                          'conscientiousness', 'extraversion', 'agreeableness']

    # Generate random values for each personality trait between 0 and 100

    personality_values = {}
    accumulate = 0
    for trait in personality_traits:
        personality_values[trait] = random.randint(0, 100 - accumulate)
        accumulate += personality_values[trait]
    personality_values['agreeableness'] += 100 - accumulate

    def shoot():
        print("Shooting")

    def search():
        print("Searching")

    def talk():
        print("Talking")

    # Create the Turret class dynamically with the methods
    Turret = type('Turret', (), {
        'shoot': shoot,
        'search': search,
        'talk': talk,
        'personality_values': personality_values
    })

    return Turret


if __name__ == "__main__":
    c = turrets_generator()
    c.shoot()
    c.search()
    c.talk()
    print(*c.personality_values.values())
