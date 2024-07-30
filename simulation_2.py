import random
from armaments import F22, Rafale, F16, Gripen

def calculate_missile_combat_value(speed, accuracy, range):
    return (speed * 0.4) + (accuracy * 0.4) + (range * 0.2)

def calculate_fighter_combat_value(maneuverability, speed, defense):
    return (maneuverability * 0.4) + (speed * 0.4) + (defense * 0.2)

def calculate_total_combat_value(missile_value, fighter_value):
    return (1.3 * fighter_value) + missile_value

def roll_dice(num_rolls):
    return sum(random.randint(1, 6) for _ in range(num_rolls))

def turn_based_combat(player1_value, player2_value):
    player1_rolls = int(player1_value)
    player2_rolls = int(player2_value)

    player1_score = roll_dice(player1_rolls)
    player2_score = roll_dice(player2_rolls)

    return player1_score, player2_score

def resolve_combat(player1_score, player2_score):
    if player1_score > player2_score:
        return 1
    elif player2_score > player1_score:
        return 2
    else:
        return 0

def start_fighting(fighter1, fighter2):
    score1 = 0
    score2 = 0
    for round in range(0,1):
        random_missile = random.randint(0,4)
        #print("random missile is ",random_missile)
        missile1 = fighter1.missiles[random_missile]
        #print(f"{fighter1.name} fired {missile1.name} at {fighter2.name}")
        missile2 = fighter2.missiles[random_missile]
        #print(f"{fighter2.name} fired {missile2.name} at {fighter1.name}")
        fighter1_speed, fighter1_maneuver, fighter1_sa = fighter1.calculate_wvr_combat_params()
        fighter2_speed, fighter2_maneuver, fighter2_sa = fighter2.calculate_wvr_combat_params()

        missile1_cv = calculate_missile_combat_value(missile1.speed, accuracy=missile1.accuracy, range=missile1.range)
        #print(f"Missile 1 score {missile1_cv}")
        fighter1_cv = calculate_fighter_combat_value(maneuverability=fighter1_maneuver, speed=fighter1_speed, defense=fighter1_sa)
        #print(f"Fighter 1 score {fighter1_cv}")

        total_value1 = calculate_total_combat_value(missile1_cv, fighter1_cv)
        #print(f"Total combat value for 1 {total_value1}")

        missile2_cv = calculate_missile_combat_value(speed=missile2.speed, accuracy=missile2.accuracy, range=missile2.range)
        #print(f"Missile 2 score {missile2_cv}")

        fighter2_cv = calculate_fighter_combat_value(maneuverability=fighter2_maneuver, speed=fighter2_speed, defense=fighter2_sa)
        #print(f"Fighter 2 score {fighter2_cv}")

        total_value2 = calculate_total_combat_value(missile2_cv, fighter2_cv)
        #print(f"Total combat value for 2 {total_value2}")


        # Engage in turn-based combat
        score_i, score_j = turn_based_combat(total_value1, total_value2)
        score1+=score_i
        score2+=score_j
        #print(f"The total scores are score1 {score1}: score2 {score2}")

    result = resolve_combat(score1, score2)
    if result==1:
        ...
        #print(f"===> {fighter1.name} downed {fighter2.name}")
    elif result==2:
        ...
        #print(f"===> {fighter2.name} downed {fighter1.name}")
    else:
        print(f"===> Both aircrafts retreated..")
    return result

count = {"1":0, "2":0, "else": 0}

rafale = Rafale()
rafale = Rafale()
f16 = F16()
f22 = F22()
gripen = Gripen()

for i in range(10000):

    result = start_fighting(rafale, gripen)
    if result==1:
        count["1"] += 1
        
    elif result==2:
        count["2"] += 1
    else:
        count["else"] += 1

print(count)
if count["1"] > count["2"]:
    print(f"{rafale.name } won the battle")
else:

    print(f"{gripen.name } won the battle")

