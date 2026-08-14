"use strict";

/*
============================================================
FIOS LIVE — CANONICAL TRUTH PROJECTION
============================================================

ONE SOURCE:
    /api/test/status

This is intentionally the same proven truth contract used by
the TEST dashboard.

runtime[]:
    operational/runtime state

monitored[]:
    real monitored modules

telemetry:
    uptime/load/health/architecture/last_event

No fake values.
No generated modules.
No second runtime.
No second service manager.
============================================================
*/

const TRUTH_API = "/api/status";


function setText(element, value) {

    if (!element) {
        return;
    }

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        element.textContent = "N/A";
        return;
    }

    element.textContent = String(value);
}


function getStatus(item) {

    if (!item) {
        return "N/A";
    }

    return item.status || "N/A";
}


/*
============================================================
RUNTIME INDEX
============================================================
*/

function indexRuntime(runtime) {

    const result = {};

    if (!Array.isArray(runtime)) {
        return result;
    }

    runtime.forEach(item => {

        if (
            item &&
            item.key
        ) {
            result[item.key] = item;
        }

    });

    return result;
}


/*
============================================================
SYSTEM MODULES
============================================================

LIVE visual layout remains unchanged.

Existing module rows are reused.

Expected:

1 Repository
2 Generator
3 Validation
4 Builder Core
5 Automation
*/

function renderModules(runtime, monitored) {

    const rows = Array.from(
        document.querySelectorAll(".module")
    );

    const realModules =
        Array.isArray(monitored)
            ? monitored.filter(item =>
                item &&
                (
                    item.key === "repository" ||
                    item.key === "generator" ||
                    item.key === "validation"
                )
            )
            : [];

    const runtimeMap =
        indexRuntime(runtime);

    const projected = [
        {
            name: "Repository",
            status:
                realModules[0]
                    ? getStatus(realModules[0])
                    : "N/A"
        },
        {
            name: "Generator",
            status:
                realModules[1]
                    ? getStatus(realModules[1])
                    : "N/A"
        },
        {
            name: "Validation",
            status:
                realModules[2]
                    ? getStatus(realModules[2])
                    : "N/A"
        },
        {
            name: "Builder Core",
            status:
                getStatus(
                    runtimeMap["builder_online"]
                )
        },
        {
            name: "Automation",
            status:
                getStatus(
                    runtimeMap["automation_online"]
                )
        }
    ];

    projected.forEach((item, index) => {

        const row = rows[index];

        if (!row) {
            return;
        }

        /*
         * Prefer the known truth-name selector.
         * Fall back to the first span.
         */
        const name =
            row.querySelector(
                '[data-truth-name="true"]'
            ) ||
            row.querySelector("span");

        const status =
            row.querySelector("b");

        setText(
            name,
            item.name
        );

        setText(
            status,
            item.status
        );

        row.dataset.truthProjected = "true";
    });
}


/*
============================================================
SYSTEM HEALTH
============================================================
*/

function renderHealth(runtime) {

    const runtimeMap =
        indexRuntime(runtime);

    const healthTargets = [
        {
            key: "running",
            id: "health-kernel"
        },
        {
            key: "brain_online",
            id: "health-ai"
        },
        {
            key: "dashboard_online",
            id: "health-data"
        }
    ];

    healthTargets.forEach(target => {

        const element =
            document.getElementById(target.id);

        if (!element) {
            return;
        }

        setText(
            element,
            getStatus(
                runtimeMap[target.key]
            )
        );

    });
}


/*
============================================================
TELEMETRY
============================================================
*/

function renderTelemetry(data) {

    if (!data) {
        return;
    }

    setText(
        document.getElementById("uptime"),
        data.uptime
    );

    setText(
        document.getElementById("load"),
        data.load === null ||
        data.load === undefined
            ? "N/A"
            : `${data.load}%`
    );

    setText(
        document.getElementById("architecture"),
        data.architecture === null ||
        data.architecture === undefined
            ? "N/A"
            : `${data.architecture}%`
    );

    setText(
        document.getElementById("last-event"),
        data.last_event
    );
}


/*
============================================================
HEADER TIME
============================================================
*/

function renderTime(timestamp) {

    if (!timestamp) {
        return;
    }

    const candidates = [
        document.getElementById("timestamp"),
        document.getElementById("system-time"),
        document.querySelector("[data-truth-time]")
    ];

    const element =
        candidates.find(Boolean);

    if (!element) {
        return;
    }

    const date =
        new Date(timestamp);

    if (
        Number.isNaN(
            date.getTime()
        )
    ) {
        setText(element, timestamp);
        return;
    }

    setText(
        element,
        date.toLocaleString()
    );
}


/*
============================================================
CANONICAL LIVE UPDATE
============================================================
*/

async function updateTruth() {

    try {

        const response =
            await fetch(
                `${TRUTH_API}?live=${Date.now()}`,
                {
                    method: "GET",
                    cache: "no-store",
                    headers: {
                        "Cache-Control": "no-cache"
                    }
                }
            );

        if (!response.ok) {
            throw new Error(
                `Truth API HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        /*
         * Canonical separation.
         */
        renderModules(
            data.runtime,
            data.monitored
        );

        renderHealth(
            data.runtime
        );

        renderTelemetry(
            data
        );

        renderTime(
            data.timestamp
        );

        document.documentElement.dataset.truthConnected =
            "true";

        document.documentElement.dataset.truthTimestamp =
            data.timestamp || "";

        console.log(
            "FIOS LIVE TRUTH CONNECTED",
            data
        );

    }
    catch (error) {

        console.error(
            "FIOS LIVE Truth API error:",
            error
        );

        document.documentElement.dataset.truthConnected =
            "false";
    }
}


/*
============================================================
START
============================================================
*/

updateTruth();

setInterval(
    updateTruth,
    2000
);