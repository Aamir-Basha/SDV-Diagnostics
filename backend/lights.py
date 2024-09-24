import time
import json
import sys

class LightsECU:
    def __init__(self):
        self.headlights = False
        self.taillights = False

    def toggle_headlights(self):
        self.headlights = not self.headlights
        return self.get_status()

    def toggle_taillights(self):
        self.taillights = not self.taillights
        return self.get_status()

    def get_status(self):
        return {
            'headlights': 'On' if self.headlights else 'Off',
            'taillights': 'On' if self.taillights else 'Off'
        }

if __name__ == "__main__":
    lights = LightsECU()
    while True:
        status = lights.get_status()
        print(json.dumps(status))
        sys.stdout.flush()
        command = sys.stdin.readline().strip()
        if command == 'toggle_headlights':
            status = lights.toggle_headlights()
            print(json.dumps(status))
            sys.stdout.flush()
        elif command == 'toggle_taillights':
            status = lights.toggle_taillights()
            print(json.dumps(status))
            sys.stdout.flush()
        else:
            status = lights.get_status()
            print(json.dumps(status))
            sys.stdout.flush()
        time.sleep(1)
