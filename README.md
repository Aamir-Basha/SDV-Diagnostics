
# Software-Defined Vehicle (SDV) Diagnostics Dashboard

## Project Overview

This project showcases a fully functional diagnostics dashboard for a Software-Defined Vehicle (SDV) simulation. The aim is to simulate a modern vehicle diagnostics system, focusing on real-time data monitoring and control of various vehicle systems, including engine speed, RPM, throttle, lights, and braking.

The project integrates Python for backend vehicle logic and diagnostics and Node.js (Express + Socket.IO) for real-time communication between the backend and the frontend. The dashboard is built using HTML, CSS, and JavaScript, with dynamic elements to visualize the speed, RPM, and other metrics using gauges and indicators.

## Key Features

- **Real-time Monitoring**: Real-time updates for engine speed, RPM, throttle, gear, and battery status.
- **Interactive Controls**: Toggle headlights, taillights, apply throttle, and braking through the dashboard.
- **Diagnostics Module**: Displays live error diagnostics, and logs the error history.
- **Smooth Needle Animation**: A smooth, real-time needle animation for the speed gauge that reacts dynamically based on engine speed data.
- **Braking and Charging Simulation**: Simulates vehicle braking and charging behavior.

## Technical Stack

- **Backend**: Python for handling engine logic and generating diagnostic data.
- **Frontend**: HTML, CSS, and JavaScript for a responsive dashboard with real-time updates.
- **Server**: Node.js (Express + Socket.IO) for server-side communication and real-time data transfer.

## How It Works

1. **Backend (engine.py)**: Simulates vehicle components (engine, speed, battery, diagnostics) and generates live data.
2. **Server (app.js)**: Handles communication between Python backend and the frontend using Socket.IO. Sends data from the backend to the frontend for live updating of dashboard components.
3. **Frontend (index.html)**: Visualizes the vehicle's data using gauges for speed, RPM, and other controls for lights, throttle, and brakes.


## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone git@github.com:Aamir-Basha/SDV-Diagnostics.git
   ```

2. Install dependencies in the server folder:
   ```bash
   cd SDV-Diagnostics/server
   sudo npm install express socket.io
   ```

## Running the Application

- To start the application, run the following command in the server directory:
   ```bash
   node app.js
   ```

- After starting the application, open your web browser and navigate to:
   ```bash
   http://localhost:8888
   ```



## Key Components

- **Speed Gauge**: The speed gauge dynamically updates with data received from the engine simulation.
- **Diagnostics Panel**: Displays any errors and logs error history for later analysis.
- **Throttle and Brake Controls**: Interactively control the vehicle's throttle and brakes, simulating acceleration and deceleration.
- **Battery Status**: Monitors and displays the battery's charging state.

## Future Enhancements

While this project is currently a proof of concept, my intention is to evolve it into a real-world project by further enhancing its features and capabilities. Future enhancements could include:

- **Integration with real vehicle data**: Moving from simulation to actual vehicle diagnostics using real-time vehicle data.
- **Advanced Analytics**: Implement machine learning algorithms for predictive diagnostics.
- **Cloud Integration**: Store diagnostics data in the cloud for remote access and analysis.
- **Mobile Interface**: Develop a mobile version of the dashboard for easier, remote vehicle monitoring.

---

**Disclaimer**: This project is a proof of concept with the intent to evolve it into a real-world system.

