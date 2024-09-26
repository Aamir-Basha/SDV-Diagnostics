const socket = io();

socket.on('lights-status', (data) => {
    const lightsData = JSON.parse(data);
    document.getElementById('headlights').innerText = lightsData.headlights;
    document.getElementById('taillights').innerText = lightsData.taillights;
});


function toggleHeadlights() {
    socket.emit('toggle-headlights');
}

function toggleTaillights() {
    socket.emit('toggle-taillights');
}



function updateThrottle() {
    const throttleValue = document.getElementById('throttleSlider').value;
    document.getElementById('throttleValue').innerText = throttleValue;
}

function applyThrottle() {
    const throttleValue = document.getElementById('throttleSlider').value;
    socket.emit('set-throttle', { throttle: throttleValue });
    console.log(`Emitting throttle value: ${throttleValue}`);
}

document.getElementById('clearDataButton').addEventListener('click', () => {
    socket.emit('clear-the-data');
});

socket.on('engine-status', (data) => {
    try {
        const status = JSON.parse(data);
        document.getElementById('rpm').innerText = status.rpm;
        document.getElementById('speed').innerText = status.speed;
        document.getElementById('gear').innerText = status.gear;
        document.getElementById('temperature').innerText = status.temperature;
        document.getElementById('throttle').innerText = status.throttle;
    } catch (error) {
        console.error("Failed to parse engine status:", error);
    }
});

