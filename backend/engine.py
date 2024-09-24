import time
import random
import json
import sys

class EngineECU:
    def __init__(self):
        # Initializing engine parameters
        self.rpm = 2000
        self.temperature = 75.0  # in °C
        self.max_rpm = 8000
        self.min_rpm = 2000
        self.rpm_change_rate = 100

    def update_rpm(self):
        # RPM changes
        if self.rpm >= self.max_rpm:
            return -self.rpm_change_rate 
        elif self.rpm <= self.min_rpm:
            return self.rpm_change_rate
        else:
            # Randomly increase or decrease RPM
            return self.rpm_change_rate if random.choice([True, False]) else -self.rpm_change_rate

    def update_temperature(self):
        fluctuation = random.uniform(-0.5, 0.5)
        self.temperature += fluctuation
        return round(self.temperature, 2)

    def get_status(self):
        # Update RPM and temperature
        self.rpm += self.update_rpm() + random.randint(0, 150)
        self.rpm = max(self.min_rpm, min(self.max_rpm, self.rpm))
        temperature = self.update_temperature()

        return {
            'rpm': self.rpm,
            'temperature': temperature
        }

if __name__ == "__main__":
    engine = EngineECU()
    try:
        while True:
            status = engine.get_status()
            print(json.dumps(status))
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the engine.")
