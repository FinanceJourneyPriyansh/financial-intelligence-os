const bootTime = Date.now();


function updateClock() {
    const now = new Date();

    document.getElementById("date").innerHTML =
        now.toLocaleDateString("en-GB");

    document.getElementById("clock").innerHTML =
        now.toLocaleTimeString();
}


function updateUptime(value) {
    const element = document.getElementById("uptime");

    if (element) {
        element.innerHTML = value;
    }
}


function updateLoad(value) {
    const element = document.getElementById("load");

    if (element) {
        element.innerHTML = value + "%";
    }
}


function updateModuleStates(modules) {
    if (!Array.isArray(modules)) {
        return;
    }

    const moduleElements =
        document.querySelectorAll(".module");

    modules.forEach((module, index) => {
        const element = moduleElements[index];

        if (!element) {
            return;
        }

        const status = module[1];

        const statusElement =
            element.querySelector("b");

        if (statusElement) {
            statusElement.innerHTML = status;
        }
    });
}


async function updateTelemetry() {
    try {
        const response =
            await fetch("/api/status", {
                cache: "no-store"
            });

        if (!response.ok) {
            throw new Error(
                "API returned " + response.status
            );
        }

        const data = await response.json();

        updateUptime(data.uptime);

        updateLoad(
            data.health
        );

        updateModuleStates(
            data.modules
        );

    } catch (error) {
        console.error(
            "FIOS telemetry error:",
            error
        );
    }
}


function heartbeat() {
    const reactor =
        document.querySelector(".core-inner");

    if (reactor) {
        reactor.style.boxShadow =
            "0 0 " +
            (70 + Math.random() * 50) +
            "px #00eaff";
    }
}


setInterval(
    updateClock,
    1000
);

setInterval(
    updateTelemetry,
    2000
);

setInterval(
    heartbeat,
    800
);


updateClock();
updateTelemetry();
