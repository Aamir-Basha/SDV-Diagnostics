const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { spawn } = require('child_process');
const path = require('path'); 

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static(path.join(__dirname, '../frontend')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/public', 'index.html'));
});

let currentThrottle = 0;
let lightsProcess;

function runECU(scriptName) {
    console.log(`Starting ${scriptName}...`);

   const scriptPath = path.join(__dirname, '../backend/', `${scriptName}.py`);

    const process = spawn('python3.10', ['-u', scriptPath], { cwd: path.join(__dirname, '../backend/') });

    process.stdout.on('data', (data) => {
        const parsedData = data.toString().trim();
        if (parsedData) {
            console.log(`Data from ${scriptName}: ${parsedData}`);
            io.emit(`${scriptName}-status`, parsedData);
        } else {
            console.log(`No data received from ${scriptName}`);
        }
    });

    process.stderr.on('data', (data) => {
        console.error(`Error in ECU ${scriptName}: ${data}`);
    });

    process.on('exit', (code) => {
        console.log(`${scriptName}.py exited with code ${code}`);
    });

    process.on('error', (err) => {
        console.error(`Failed to start subprocess for ${scriptName}:`, err);
    });

    return process;
}

const engineProcess = runECU('engine');
lightsProcess = runECU('lights');
const diagnosticsProcess = runECU('diagnostics');

io.on('connection', (socket) => {
    console.log('Client connected');


    engineProcess.stdin.write(`clear_the_data\n`);

    socket.on('clear-the-data', () => {
        console.log('Clearing engine data');

        if (engineProcess && engineProcess.stdin) {
            engineProcess.stdin.write('clear_the_data\n');
        }
    });


    lightsProcess.stdin.write('toggle_headlights\n');

    socket.on('set-throttle', (data) => {
        console.log(`Throttle set to: ${data.throttle}`);
        currentThrottle = data.throttle;

        if (engineProcess && engineProcess.stdin) {
            engineProcess.stdin.write(`set_throttle ${currentThrottle}\n`);
        }
    });

    socket.on('toggle-headlights', () => {
        console.log('Toggle headlights command received');
        if (lightsProcess) {
            lightsProcess.stdin.write('toggle_headlights\n');
        }
    });

    socket.on('toggle-taillights', () => {
        console.log('Toggle taillights command received');
        if (lightsProcess) {
            lightsProcess.stdin.write('toggle_taillights\n');
        }
    });
});

let port = 8888;
server.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
