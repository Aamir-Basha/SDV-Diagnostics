import time
import json
import sys
import threading

class EngineECU:
    def __init__(self):
        self.rpm = 800  
        self.speed = 0  
        self.gear = 1  
        self.throttle = 0  # In %
        self.temperature = 75.0  # In C
        self.simulating = False
        
        self.battery_level = 80  # In %
        self.is_charging = False

        self.is_braking = False

        self.gear_speed_ranges = {
            1: (0, 20),
            2: (20, 40),
            3: (40, 60),
            4: (60, 80),
            5: (80, 120),
            6: (120, 180)
        }

        self.gear_rpm_ranges = {
            1: (800, 2000),
            2: (1000, 2500),
            3: (2000, 3000),
            4: (2500, 3500),
            5: (3000, 4000),
            6: (4000, 8000)
        }

        self.gear_shift_delay = 0.3
        self.battery_level = 80
        self.is_charging = False

    def apply_throttle(self):
        if self.throttle > 0:
            self.is_braking = False
            min_rpm, max_rpm = self.gear_rpm_ranges[self.gear]
            rpm_increase = self.throttle * 5
            self.rpm = min(self.rpm + rpm_increase, max_rpm)
        else:
            self.is_braking = True

        self.battery_level = max(0, self.battery_level - (self.throttle / 100) * 0.1)


    def apply_brake(self):
        self.throttle = 0
        while self.speed > 0:
            self.rpm = max(800, self.rpm - 200)
            self.speed = max(0, self.speed - 5)
            time.sleep(0.03)
            print(json.dumps(self.get_status()))
            sys.stdout.flush()

    def update_speed(self):
        min_speed, max_speed = self.gear_speed_ranges[self.gear]
        min_rpm, max_rpm = self.gear_rpm_ranges[self.gear]

        self.speed = ((self.rpm - min_rpm) / (max_rpm - min_rpm)) * (max_speed - min_speed) + min_speed
        return round(self.speed, 2)

    def shift_gears(self):
        min_rpm, max_rpm = self.gear_rpm_ranges[self.gear]
        min_speed, max_speed = self.gear_speed_ranges[self.gear]

        if self.rpm >= max_rpm and self.speed >= max_speed:
            if self.gear < 6:
                self.gear += 1
                self.rpm = self.gear_rpm_ranges[self.gear][0]
                time.sleep(self.gear_shift_delay)
            else:
                self.rpm = max_rpm
                self.speed = max_speed
        elif self.rpm < self.gear_rpm_ranges[self.gear][0] and self.gear > 1:
            self.gear -= 1
            self.rpm = self.gear_rpm_ranges[self.gear][1]

    def update_temperature(self):
        if self.temperature < 120:
            temp_rise = (self.rpm / 8000) * 4
            self.temperature += temp_rise
            
        if self.rpm < 1000 and self.temperature < 120:
            self.temperature -= 0.5
        return round(self.temperature, 2)

    def update_battery_usage(self):
        if not self.is_charging:
            usage_rate = self.throttle * 0.005
            self.battery_level = max(0, self.battery_level - usage_rate)
            self.battery_level = round(self.battery_level, 2)
    
    def regenerate_battery(self):
        regen_rate = 2
        self.battery_level = min(100, self.battery_level + regen_rate)

    def start_charging(self):
        self.is_charging = True
        while self.battery_level < 100:
            self.battery_level += 2

            time.sleep(1)
            status = self.get_status()
            save_data(status)
            print(json.dumps(status))
            sys.stdout.flush()

        self.is_charging = False
        status = self.get_status()
        save_data(status)
        print(json.dumps(status))
        sys.stdout.flush()
        print('Battery fully charged')

    def full_throttle_simulation(self):
        while self.simulating:
            self.apply_throttle()
            if self.is_braking:
                self.apply_brake()
            self.shift_gears()
            speed = self.update_speed()
            temperature = self.update_temperature()

            status = self.get_status()
            save_data(status)
            print(json.dumps(status))
            sys.stdout.flush()
            
            time.sleep(1)

    def clear_data(self):
        self.rpm = 800
        self.speed = 0
        self.gear = 1
        self.throttle = 0
        self.temperature = 75.0
        self.battery_level = 80


    def get_status(self):
        self.apply_throttle()
        self.shift_gears()
        speed = self.update_speed()
        temperature = self.update_temperature()

        return {
            'rpm': int(self.rpm),
            'gear': self.gear,
            'speed': speed,
            'temperature': temperature,
            'throttle': self.throttle,       
            'is_braking': self.is_braking,
            'battery-value-1': round(self.battery_level, 2),
            'is_charging' : self.is_charging
        }

def save_data(status):
    with open('engine_data.json', 'a') as f:
        f.write(json.dumps(status) + "\n")

if __name__ == "__main__":
    engine = EngineECU()

    while True:
        command = sys.stdin.readline().strip()

        if command.startswith('clear_the_data'):
            engine.clear_data()
            status_engnie = engine.get_status()
            save_data(status_engnie)
            print(json.dumps(status_engnie))
            sys.stdout.flush()
            engine.simulating = False
            engine.is_charging = False

        if command.startswith('set_throttle'):
            engine.simulating = True
            _, throttle_value = command.split()
            engine.throttle = max(0, min(100, float(throttle_value)))
            threading.Thread(target=engine.full_throttle_simulation).start()

        if command.startswith('apply_brake'):
            engine.simulating = False
            engine.apply_brake()

        if command.startswith('chargeBattery'):
            if not engine.simulating:
                threading.Thread(target=engine.start_charging()).start()
                engine.is_charging = False
                status_engnie = engine.get_status()
                save_data(status_engnie)
                print(json.dumps(status_engnie))
                sys.stdout.flush()

            else: 
                print("Cannot charge while in Throttle")
        



        time.sleep(1)
