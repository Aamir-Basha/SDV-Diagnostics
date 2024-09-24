const socket = io();

socket.on('engine-status', (data) => {
    const engineData = JSON.parse(data);
    document.getElementById('rpm').innerText = engineData.rpm;
    document.getElementById('temperature').innerText = engineData.temperature;
});

socket.on('lights-status', (data) => {
    const lightsData = JSON.parse(data);
    document.getElementById('headlights').innerText = lightsData.headlights;
    document.getElementById('taillights').innerText = lightsData.taillights;
});

socket.on('diagnostics-status', (data) => {
    const diagnosticsData = JSON.parse(data);
    document.getElementById('errors').innerText = diagnosticsData.errors.join(', ');
});

function toggleHeadlights() {
    socket.emit('toggle-headlights');
}

function toggleTaillights() {
    socket.emit('toggle-taillights');
}
