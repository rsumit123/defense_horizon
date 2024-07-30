import random
from armaments import Fighter
from armaments import F22
from armaments import GeneralElectricF404
from armaments import Aim09Sidewinder, Aim120Amraam, ANAPG65, ElectronicCounterMeasures



import random



def check_for_malfunctions(fighter):
    print(f"Malfunction ratio of {fighter.name} is {fighter.maintenance_ratio}")
    malfunction_chance = 1 - fighter.maintenance_ratio  # Higher chance with poor maintenance
    random_mal_chance = random.random()
    print("Random mal chance is ",random_mal_chance)
    print(f"Malfunction chance of {fighter.name} is {malfunction_chance}")
    if random_mal_chance < malfunction_chance:
        print(f"Fighter {fighter.name} has malfunctioned, decreased performance")
        print(f"{fighter.name} experiences a malfunction!")
        fighter.speed *= 0.8  # Reduce speed due to malfunction
        for missiles in fighter.missiles:
            missiles.speed *= 0.8
        # Other penalties...


def fight_with_missiles(fighter1, fighter2, weather, engagement_type):
    """
    Determines the outcome of a missile engagement between two fighters.
    
    Args:
    fighter1, fighter2 (Fighter): Instances of Fighter class representing the jets.
    
    Returns:
    str: Report of missile engagement results.
    """
    check_for_malfunctions(fighter1)
    check_for_malfunctions(fighter2)

    fighter1_score = {"hits": 0, "misses": 0}
    fighter2_score = {"hits": 0, "misses": 0}


    report = []
    missile_speed = {missile.name: missile.speed for missile in fighter1.missiles + fighter2.missiles}

    # Fighter 1 attacks Fighter 2
    for missile in fighter1.missiles:
        evasion_chance = calculate_evasion_chance(fighter2, missile, missile_speed[missile.name], engagement_type)
        hit_chance = calculate_hit_chance(missile, fighter2, weather, engagement_type)
        print(f"Hit chance is {hit_chance}")
        print(f"Evasion chance is {evasion_chance}")
        if hit_chance > evasion_chance:  # Random factor to decide if the missile hits
            print(f"{fighter1.name} successfully hits {fighter2.name} with a {missile.name}.")
            report.append(f"{fighter1.name} successfully hits {fighter2.name} with a {missile.name}.")
            fighter1_score["hits"] += 1
        else:
            print(f"{fighter2.name} evades a {missile.name} fired by {fighter1.name}.")
            report.append(f"{fighter2.name} evades a {missile.name} fired by {fighter1.name}.")
            fighter1_score["misses"] += 1

    # Fighter 2 attacks Fighter 1
    for missile in fighter2.missiles:
        hit_chance = calculate_hit_chance(missile, fighter1, weather, engagement_type)
        evasion_chance = calculate_evasion_chance(fighter1, missile, missile_speed[missile.name], engagement_type)
        if hit_chance > evasion_chance:
            report.append(f"{fighter2.name} successfully hits {fighter1.name} with a {missile.name}.")
            fighter2_score["hits"] += 1
        else:
            report.append(f"{fighter1.name} evades a {missile.name} fired by {fighter2.name}.")
            fighter2_score["misses"] += 1

    return "\n".join(report), [fighter1_score, fighter2_score]

def aoa_impact(angle_of_attack):
    """
    Calculates a dynamic impact factor based on the angle of attack (AoA).
    The impact increases with higher AoA but caps at a certain point to avoid unrealistic outcomes.

    Args:
    angle_of_attack (float): The current angle of attack of the fighter in degrees.

    Returns:
    float: A multiplier for evasion and hit probability adjustments.
    """
    # Scale the AoA impact linearly up to a cap of 30 degrees, beyond which it remains constant.
    if angle_of_attack <= 30:
        return 1 + (angle_of_attack / 30) * 0.2  # up to 20% increase at 30 degrees
    else:
        return 1.2  # Cap the impact to avoid excessive influence

def calculate_evasion_chance(target_fighter, missile, missile_speed, engagement_type):
    """
    Adjusted to increase base evasion and enhance AoA and ECM impacts.
    """
    if engagement_type == 'BVR':
        distance = random.uniform(20, 100)
    else:
        distance = random.uniform(0, 20)

    speed_ratio = target_fighter.speed / missile_speed
    maneuver_factor = 1.2 if target_fighter.engine.thrust_vectoring else 1.0
    aoa_factor = aoa_impact(target_fighter.angle_of_attack)

    

    if engagement_type == 'WVR':

        random_factor_wvr = random.uniform(0.7,1.3)

        evasion_chance = 0.45*random_factor_wvr - (speed_ratio - 1) * 0.05
        
        evasion_chance *= maneuver_factor * aoa_factor * 1.2
        # print("wvr fight=====",evasion_chance)
        
    else:
        random_factor_bvr = random.uniform(0.8,1.2)
        # Increased base evasion chance
        evasion_chance = 0.7*random_factor_bvr - (speed_ratio - 1) * 0.05
        ecm = target_fighter.ecm if hasattr(target_fighter, 'ecm') else ElectronicCounterMeasures()
        evasion_chance *= 0.8 * ecm.effectiveness * ecm.stealth_factor * aoa_factor
        if distance > ecm.jamming_range:
            evasion_chance *= 0.7

    return min(max(evasion_chance, 0.1), 0.9)

def calculate_hit_chance(missile, target_fighter, weather, engagement_type):
    """
    Reduced base hit chance and increased variability.
    """
    base_hit_chance = 0.75 if missile.guidance == "radar" else 0.65
    ecm_effectiveness = target_fighter.ecm.effectiveness if hasattr(target_fighter, 'ecm') else 0.5
    aoa_factor = aoa_impact(target_fighter.angle_of_attack)

    hit_chance = base_hit_chance * (1 - ecm_effectiveness) * aoa_factor

    if weather['visibility'] < 5:
        hit_chance *= 0.75

    if engagement_type == 'BVR':
        hit_chance *= 0.85
    else:
        hit_chance *= 1.05

    hit_chance += random.uniform(-0.15, 0.15)
    return max(min(hit_chance, 0.95), 0.05)

def simulate_fighter_engagement(fighter1, fighter2, weather, engagement_type="WVR"):
    """
    Simulates an engagement between two fighter jets with detailed considerations for BVR and WVR combat scenarios.
    Incorporates dynamic missile engagement modeling.
    
    Args:
    fighter1, fighter2 (Fighter): Fighter class instances representing the jets.
    weather (dict): Dictionary containing weather conditions like 'visibility' and 'wind'.
    engagement_type (str): Type of engagement, "WVR" or "BVR".
    
    Returns:
    str: Detailed report of the engagement.
    """
    # Initial report and setup for missile combat
    missile_report, scores = fight_with_missiles(fighter1, fighter2, weather, engagement_type)

    # Calculate total effectiveness based on missile hits vs misses
    effectiveness1 = scores[0]["hits"] - scores[0]["misses"]
    effectiveness2 = scores[1]["hits"] - scores[1]["misses"]

    # Adjust effectiveness for radar and AoA if it's a BVR engagement
    if engagement_type == 'BVR':
        effectiveness1 += (fighter1.radar.range / 10) * (fighter1.angle_of_attack / 20)
        effectiveness2 += (fighter2.radar.range / 10) * (fighter2.angle_of_attack / 20)

    # Append missile combat results to the report
    report = [missile_report]

    print(f"{fighter1.name} effectiveness is {effectiveness1}")
    print(f"{fighter2.name} effectiveness is {effectiveness2}")


    # Determine the winner based on modified effectiveness
    if effectiveness1 > effectiveness2:
        report.append(f"{fighter1.name} wins the engagement!")
    else:
        report.append(f"{fighter2.name} wins the engagement!")

    return "\n".join(report)

# Example usage of the function
# You would need to pass actual instances of `Fighter`, weather conditions, and specify the engagement type.

# Assuming you have instances of fighters ready with similar setups
f22 = F22()
f22.maintenance_ratio = 0.5
f22_2 = F22()
f22_2.maintenance_ratio = 0.5

rafale = Fighter(name='Rafale', engine=GeneralElectricF404(), radar=ANAPG65(), speed=2000)
rafale.add_missile(Aim120Amraam(), 2)  # Just an example setup
rafale.add_missile(Aim09Sidewinder(), 2)

weather = {'visibility': 8, 'wind': 3}

# Run simulation
print(simulate_fighter_engagement(f22, f22_2, weather, engagement_type="WVR"))
