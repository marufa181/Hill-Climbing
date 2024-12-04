# -*- coding: utf-8 -*-
"""hill climbing by Utsho sir.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rF-f3mw2PWas2aW2zzjbFy3kMc5n5kbd
"""

'''

You have a car.
A car is made of an engine, a transmission, a tire, and a roof.
Engine choice: engines.txt file
Tire choices: tires.txt file
Transmission choices: transmissions.txt file
Roof choices: Sunroof, Moonroof, No roof

                                                         Engine Tire Transmission Roof
You have a car like START STATE (EFI,Danlop,AT,Noroof)
You want to have a car like GOAL STATE   (V12,Pirelli,CVT,Sunroof)
Each year you can change only 1 component of the car which results in a way that makes a valid car model i.e You can’t change your component in a way which makes your car invalid at any point of time. The valid car models are given in the valid_book.csv file.
You want to have your dream car as soon as possible i.e Minimize the years after which you get your desired car..

How to calculate the cost between two states: Number of mismatched components.
Example: ΔE = 3 for  (EFI,Danlop,AT,Noroof) and  (EFI,Danlop,AT,Sunroof) as only the roof state mismatches.


If at any point, you arrive at an invalid state, you  can’t go any further from that one, just discard that state.



Probability function for simulated annealing: e^(ΔE/t) [Note: this function is required only when ΔE is negative]
Here, ΔE = next_node.val - current_node.val
Y = year passed aka BFS level
t = 1 / Y

Override __hash__ method of Car class [Ref: https://stackoverflow.com/questions/2909106/whats-a-correct-and-good-way-to-implement-hash
]


Probability modeling:

random.uniform(0, 1) <=  e

'''


import random
import csv
from math import exp

class Car:
    def __init__(self, engine, tire, transmission, roof):
        self.engine = engine
        self.tire = tire
        self.transmission = transmission
        self.roof = roof

    def __hash__(self):
        return hash((self.engine, self.tire, self.transmission, self.roof))

    def __eq__(self, other):
        return (self.engine, self.tire, self.transmission, self.roof) == (other.engine, other.tire, other.transmission, other.roof)

def get_valid_states():
    valid_states = set()
    with open('/content/valid_book.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            engine, tire, transmission, roof = row
            valid_states.add(Car(engine, tire, transmission, roof))
    return valid_states

def get_random_choice(choices):
    return random.choice(choices)

def get_engine_choices():
    with open('/content/engines.txt', 'r') as file:
        return file.read().splitlines()

def get_tire_choices():
    with open('/content/tires.txt', 'r') as file:
        return file.read().splitlines()

def get_transmission_choices():
    with open('/content/transmissions.txt', 'r') as file:
        return file.read().splitlines()

def calculate_cost(current_state, goal_state):
    cost = 0
    if current_state.engine != goal_state.engine:
        cost += 1
    if current_state.tire != goal_state.tire:
        cost += 1
    if current_state.transmission != goal_state.transmission:
        cost += 1
    if current_state.roof != goal_state.roof:
        cost += 1
    return cost

def simulated_annealing(current_state, goal_state):
    valid_states = get_valid_states()
    current_cost = calculate_cost(current_state, goal_state)
    temperature = 1.0
    cooling_rate = 0.9
    year = 0

    while current_cost > 0:
        year += 1
        temperature /= year

        new_state = Car(
            get_random_choice(get_engine_choices()),
            get_random_choice(get_tire_choices()),
            get_random_choice(get_transmission_choices()),
            get_random_choice(["Sunroof", "Moonroof", "No roof"])
        )

        if new_state in valid_states:
            new_cost = calculate_cost(new_state, goal_state)
            cost_diff = new_cost - current_cost

            if cost_diff < 0 or (cost_diff > 0 and random.uniform(0, 1) <= exp(-cost_diff / temperature)):
                current_state = new_state
                current_cost = new_cost

        if year >= 1000 or temperature <= 1e-6:
            break

    return current_state, year


start_state = Car("EFI", "Danlop", "AT", "Noroof")
goal_state = Car("V12", "Pirelli", "CVT", "Sunroof")

final_state, years = simulated_annealing(start_state, goal_state)

if years <= 1000:
    print("Goal state:", goal_state.__dict__)
    print("Goal state reached in", years, "years.")
else:
    print("Failed to reach the goal state within the given constraints.")