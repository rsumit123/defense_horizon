class Engine:
    def __init__(self, thrust=100, thrust_vectoring=False):
        self.thrust = thrust
        self.thrust_vectoring = thrust_vectoring
    
class SnecmaM88(Engine):
    def __init__(self):
        super().__init__(thrust=75, thrust_vectoring=False)

class ElectronicCounterMeasures:
    def __init__(self, effectiveness=0.5, jamming_range=45, stealth_factor=0.5):
        """
        Initializes the ECM capabilities of a fighter.

        Args:
        effectiveness (float): A value between 0 and 1 representing how effective the ECM is at disrupting enemy sensors and missiles.
        jamming_range (int): The range in kilometers over which the ECM can effectively jam enemy radars and communications.
        stealth_factor (float): A value between 0 and 1 representing the reduction in radar cross-section due to stealth technologies.
        """
        self.effectiveness = effectiveness
        self.jamming_range = jamming_range
        self.stealth_factor = stealth_factor

    def describe(self):
        """Prints a description of the ECM capabilities."""
        print(f"ECM Effectiveness: {self.effectiveness * 100}%")
        print(f"Jamming Range: {self.jamming_range} km")
        print(f"Stealth Factor: {self.stealth_factor * 100}% Reduction")


class PrattWhitneyF119(Engine):
    def __init__(self):
        super().__init__(thrust=156, thrust_vectoring=True)

class GeneralElectricF404(Engine):
    def __init__(self):
        super().__init__(thrust=85, thrust_vectoring=False)

class Radar:
    def __init__(self, range=150, detection_range=100):
        self.range = range
        self.detection_range = detection_range

class ANAPG77(Radar):
    def __init__(self):
        super().__init__(range=200, detection_range=250)

class RBE2AESA(Radar):
    def __init__(self):
        super().__init__(range=200, detection_range=200)

class ANAPG65(Radar):
    def __init__(self):
        super().__init__(range=150, detection_range=120)

class Missile:
    def __init__(self, name='Generic', range=100, guidance='IR', speed=1300, weight=80, accuracy=0.7):
        self.name = name
        self.range = range
        self.guidance = guidance
        self.speed = speed # Speed in km/hr
        self.weight = weight
        self.accuracy = accuracy

# class Missile:
#     def __init__(self, name, range, guidance, weight, accuracy, speed):
#         self.name = name
#         self.range = range
#         self.guidance = guidance
#         self.weight = weight
#         self.accuracy = accuracy
#         self.speed = speed

class Aim120Amraam(Missile):
    def __init__(self):
        super().__init__(name="AIM-120 AMRAAM", range=120, guidance="radar", weight=152, accuracy=0.9, speed=4900)

class Aim09Sidewinder(Missile):
    def __init__(self):
        super().__init__(name="AIM-9 Sidewinder", range=35, guidance="IR", weight=85, accuracy=0.85, speed=2575)

class Mica(Missile):
    def __init__(self):
        super().__init__(name="MICA", range=80, guidance="dual (radar/IR)", weight=112, accuracy=0.88, speed=3600)

class MBDAAsraam(Missile):
    def __init__(self):
        super().__init__(name="MBDA ASRAAM", range=50, guidance="IR", weight=88, accuracy=0.92, speed=3500)

class ScalpEg(Missile):
    def __init__(self):
        super().__init__(name="SCALP EG", range=250, guidance="GPS/INS", weight=1300, accuracy=0.95, speed=1000)

class MbdaMeteor(Missile):
    def __init__(self):
        super().__init__(name="MBDA Meteor", range=150, guidance="active radar", weight=190, accuracy=0.95, speed=4700)


class Fighter:
    def __init__(self, name='Generic Fighter', engine=None, radar=None, ecm=None, slots=5, angle_of_attack=30, speed=1100, maintenance_ratio=0.95, weight=15000):
        self.name = name
        self.engine = engine if engine else Engine()
        self.radar = radar if radar else Radar()
        self.missiles = []
        self.slots = slots
        self.angle_of_attack = angle_of_attack
        self.weight = weight  # in kg
        self.speed = speed
        self.ecm = ecm if ecm else ElectronicCounterMeasures()
        self.maintenance_ratio = maintenance_ratio
        self.total_weight = self.weight

    def add_missile(self, missile, quantity=1):
        if len(self.missiles) + quantity <= self.slots:
            self.missiles.extend([missile] * quantity)
            for miss in self.missiles:
                self.total_weight += miss.weight
        else:
            raise ValueError("Slots full")

    def calculate_wvr_combat_params(self):
        # Normalize parameters
        def normalize(value, min_value, max_value):
            # Ensure no division by zero
            if max_value == min_value:
                return 1
            #return 
            normalized = 1 + 9 * (value - min_value) / (max_value - min_value)
            return max(1, min(normalized, 10))
                       

        # Example bounds (these can be adjusted based on the data range of all fighters)
        speed_min, speed_max = 500, 3500  # Min and max speeds in km/h
        maneuver_min, maneuver_max = 0.72, 1.46  # Calculated bounds for maneuverability
        sa_min, sa_max = 0.8, 3.9  # Calculated bounds for situational awareness

        # Thrust-to-Weight Ratio
        thrust_weight_ratio = (self.engine.thrust * 1000) / (self.total_weight * 9.8)
        # print(f"Thrust w ratio is {thrust_weight_ratio}")
        # print(f"The AoA is {self.angle_of_attack}")

        # Maneuverability: Directly related to angle of attack, directly related to thrust-to-weight ratio
        maneuver = (thrust_weight_ratio / 2) + (self.angle_of_attack / 90)
        maneuver_normalized = normalize(maneuver, maneuver_min, maneuver_max)

        # Situational Awareness
        situation_awareness = (
            (self.radar.detection_range / 200)
            + (self.ecm.jamming_range / 100)
            + (1 - self.ecm.stealth_factor)
        )
        situation_awareness_normalized = normalize(situation_awareness, sa_min, sa_max)

        # Speed
        speed_normalized = normalize(self.speed, speed_min, speed_max)

        return (
            speed_normalized,
            maneuver_normalized,
            situation_awareness_normalized
        )
    
    

    def describe(self):
        print(f"{self.name} Specifications:")
        print(f"  Engine Thrust: {self.engine.thrust} kN, Thrust Vectoring: {'Yes' if self.engine.thrust_vectoring else 'No'}")
        print(f"Total weight of aircraft is {self.total_weight}")
        print(f"  Radar Range: {self.radar.range} km, Detection Range: {self.radar.detection_range} km")
        missile_summary = {}
        for missile in self.missiles:
            if missile.name not in missile_summary:
                missile_summary[missile.name] = 0
            missile_summary[missile.name] += 1
        print("  Missiles:")
        for name, count in missile_summary.items():
            print(f"    {name}: Quantity {count}")

class F22(Fighter):
    def __init__(self):
        super().__init__(name='F-22 Raptor',
                         engine=PrattWhitneyF119(),
                         radar=ANAPG77(), weight=19700, angle_of_attack=60)
        self.add_missile(Aim120Amraam(), 3)
        self.add_missile(Aim09Sidewinder(), 2)

class Rafale(Fighter):
    def __init__(self):
        super().__init__(name='Rafale',
                         engine=SnecmaM88(),
                         radar=RBE2AESA(), weight=10300, angle_of_attack=32)
        self.add_missile(MBDAAsraam(), 3)
        self.add_missile(Mica(), 2)

# Creating an instance of F22
f22 = F22()
f22.describe()
print(f22.calculate_wvr_combat_params())
