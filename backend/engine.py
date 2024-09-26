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
        self.simulating = True 

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

    def apply_throttle(self):
        if self.throttle > 0:
            min_rpm, max_rpm = self.gear_rpm_ranges[self.gear]
            
            rpm_increase = self.throttle * 5
            self.rpm = min(self.rpm + rpm_increase, max_rpm)

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
            self.rpm = self.gear_rpm_ranges[self.gear][1]  # Set to max RPM for downshift

    def update_temperature(self):
        temp_rise = (self.rpm / 8000) * 4
        self.temperature += temp_rise
        
        if self.rpm < 1000:
            self.temperature -= 0.5
        return round(self.temperature, 2)

    def full_throttle_simulation(self):
        while self.simulating == True:
            self.apply_throttle()
            self.shift_gears()
            speed = self.update_speed()
            temperature = self.update_temperature()
            if self.speed >= 180:
                self.simulating = False

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
            'throttle': self.throttle
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
            

        if command.startswith('set_throttle'):
            engine.simulating = True
            _, throttle_value = command.split()
            engine.throttle = max(0, min(100, float(throttle_value)))
            threading.Thread(target=engine.full_throttle_simulation).start()
    
        time.sleep(1)
