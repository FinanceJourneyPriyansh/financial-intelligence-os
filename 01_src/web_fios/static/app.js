async function updateTelemetry() {
    try {
        const res = await fetch("/api/telemetry");
        if (res.ok) {
            const data = await res.json();
            if (document.getElementById("kernel-uptime")) document.getElementById("kernel-uptime").textContent = data.uptime || "0s";
            if (document.getElementById("cpu-load")) document.getElementById("cpu-load").textContent = typeof data.cpu === "number" ? data.cpu + "%" : (data.cpu || "0%");
            if (document.getElementById("memory-ram")) document.getElementById("memory-ram").textContent = data.ram || 0;
            if (document.getElementById("stream-latency")) document.getElementById("stream-latency").textContent = data.latency || 0;
        }
    } catch (e) {
        console.error("Telemetry fetch error:", e);
    }
}

async function checkGoldStatus() {
    const badge = document.getElementById("gold-status-badge");
    if (!badge) return;
    try {
        await fetch("http://127.0.0.1:8091/", { mode: "no-cors" });
        badge.textContent = "ONLINE";
        badge.className = "status-badge online";
    } catch (err) {
        badge.textContent = "OFFLINE";
        badge.className = "status-badge offline";
    }
}

function updateClocks() {
    const now = new Date();
    const liveClock = document.getElementById("live-clock");
    const utcClock = document.getElementById("utc-clock");
    const liveDate = document.getElementById("live-date");

    if (liveClock) liveClock.textContent = now.toLocaleTimeString("en-US", { timeZone: "Asia/Kolkata", hour12: false }) + " IST";
    if (utcClock) utcClock.textContent = now.toISOString().substr(11, 8) + " UTC";
    if (liveDate) liveDate.textContent = now.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" });
}

setInterval(updateTelemetry, 2000);
setInterval(checkGoldStatus, 3000);
setInterval(updateClocks, 1000);

updateTelemetry();
checkGoldStatus();
updateClocks();
