import json
import time
import random

class DiagnosticsECU:
    def __init__(self):
        self.errors = []
        self.error_messages = [
            'None',
            'Error detected: Engine temperature too high!',
            'Error detected: Oil pressure low!',
            'Error detected: Battery voltage low!',
            'Error detected: Transmission fluid leak!',
            'Error detected: Brake system failure!',
            'Error detected: ABS malfunction!',
            'Error detected: Fuel system issue!',
            'Error detected: Airbag system error!',
            'Error detected: Tire pressure low!',
        ]

    def check_system(self):
        # Simulate random error detection with a 10% chance of generating an error
        if random.random() < 0.3:  # Change to 0.1 for a 10% chance
            error_message = random.choice(self.error_messages[1:])  # Select a random error from the list
            if error_message not in self.errors:
                self.errors.clear()

                self.errors.append(error_message)
        else:
            if 'None' not in self.errors:
                self.errors.clear()
                self.errors.append('None')


        return json.dumps({'errors': self.errors})

if __name__ == "__main__":
    diagnostics = DiagnosticsECU()
    while True:
        status = diagnostics.check_system()
        print(status)
        time.sleep(2)
