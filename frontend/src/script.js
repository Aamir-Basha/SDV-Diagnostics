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

        if (document.getElementById('rpm')) {
            document.getElementById('rpm').innerText = status.rpm;
        }

        if (document.getElementById('speed')) {
            document.getElementById('speed').innerText = status.speed;
        }

        if (document.getElementById('gear')) {
            document.getElementById('gear').innerText = status.gear;
        }

        if (document.getElementById('temperature')) {
            document.getElementById('temperature').innerText = status.temperature;
        }

        if (document.getElementById('throttle')) {
            document.getElementById('throttle').innerText = status.throttle;
        }

        
        if (document.getElementById('battery-value-1')) {
            document.getElementById('battery-value-1').innerText = status['battery-value-1'];
        }


        if (document.getElementById('braking-status')) {
            document.getElementById('braking-status').innerText = status.is_braking ? "Braking" : "Normal";
        }

        const chargingStatusElement = document.getElementById('is_charging');
        if (chargingStatusElement) {
            
            console.log('is_charging value from the front end!:', status.is_charging);
            setTimeout(() => {
                chargingStatusElement.innerText = status.is_charging ? "Charging..." : "Not charging";
            }, 100);
        }


    } catch (error) {
        console.error("Failed to parse engine status:", error);
    }
});


function applyBrake() {
    socket.emit('apply-brake');
}
function chargeBattery() {
    socket.emit('chargeBattery');
}

let errorHistory = new Set();

socket.on('diagnostics-status', (data) => {
    const diagnostics = JSON.parse(data);
    
    document.getElementById('errors').innerText = diagnostics.errors;

    if (!diagnostics.errors.includes("None")) {
        diagnostics.errors.forEach(error => errorHistory.add(error));
        
        document.getElementById('error-history').innerHTML = Array.from(errorHistory).join('<br>');
    }
});













