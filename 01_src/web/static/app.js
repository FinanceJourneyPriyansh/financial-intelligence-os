function updateFIOSClock() {
    const now = new Date();
    const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' };
    const istTimeStr = now.toLocaleTimeString('en-US', timeOptions) + ' IST';
    
    const day = String(now.getUTCDate()).padStart(2, '0');
    const monthNames = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
    const utcDateStr = ${day}-- UTC;
    const utcTimeStr = now.toISOString().substring(11, 19);

    const clockEl = document.getElementById('live-clock');
    const dateEl = document.getElementById('live-date');
    const utcEl = document.getElementById('utc-clock');

    if (clockEl) clockEl.textContent = istTimeStr;
    if (dateEl) dateEl.textContent = utcDateStr;
    if (utcEl) utcEl.textContent = utcTimeStr;
}

async function fetchTelemetry() {
    try {
        const res = await fetch('/api/telemetry');
        if (res.ok) {
            const data = await res.json();
            document.getElementById('kernel-uptime').textContent = data.uptime;
            document.getElementById('cpu-load').textContent = data.cpu;
            document.getElementById('memory-ram').textContent = data.ram;
            document.getElementById('stream-latency').textContent = data.latency;
        }
    } catch (e) {}
}

async function checkGoldSubsystem() {
    const badge = document.getElementById('gold-status-badge');
    try {
        const res = await fetch('http://127.0.0.1:8091/api/gold/snapshot', { method: 'GET' });
        if (res.ok && badge) {
            badge.textContent = 'ONLINE';
            badge.className = 'status-badge online';
        } else if (badge) {
            badge.textContent = 'OFFLINE';
            badge.className = 'status-badge offline';
        }
    } catch (e) {
        if (badge) {
            badge.textContent = 'OFFLINE';
            badge.className = 'status-badge offline';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateFIOSClock();
    setInterval(updateFIOSClock, 1000);
    
    fetchTelemetry();
    setInterval(fetchTelemetry, 2000);

    checkGoldSubsystem();
    setInterval(checkGoldSubsystem, 5000);
});
