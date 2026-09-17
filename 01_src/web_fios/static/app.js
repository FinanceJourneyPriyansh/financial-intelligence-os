async function updateTelemetry() {
    try {
        const response = await fetch('/api/telemetry');
        const data = await response.json();
        
        if (document.getElementById('clock')) {
            document.getElementById('clock').innerText = data.time;
        }
        if (document.getElementById('date')) {
            document.getElementById('date').innerText = data.date;
        }
        if (document.getElementById('automation-status')) {
            document.getElementById('automation-status').innerText = data.automation_status;
        }
        if (document.getElementById('uptime')) {
            document.getElementById('uptime').innerText = data.uptime;
        }
        if (document.getElementById('cpu')) {
            document.getElementById('cpu').innerText = data.cpu;
        }
        if (document.getElementById('ram')) {
            document.getElementById('ram').innerText = data.ram;
        }
    } catch (err) {
        console.error('Failed to fetch telemetry:', err);
    }
}

// Initial fetch and poll every 1 second
updateTelemetry();
setInterval(updateTelemetry, 1000);
