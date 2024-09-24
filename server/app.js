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


let lightsProcess;

function runECU(scriptName) {
    console.log(`Starting ${scriptName}...`);

    const process = spawn('python3.10', ['-u', `../backend/ecus/${scriptName}.py`]);

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
    lightsProcess.stdin.write('toggle_headlights\n');

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



