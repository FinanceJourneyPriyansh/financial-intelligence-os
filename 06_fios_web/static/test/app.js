"use strict";

/*
============================================================
FIOS TEST DASHBOARD — CANONICAL TRUTH PROJECTION
============================================================

ONE SOURCE:
    /api/test/status

CONTRACT:

runtime[]   = operational/runtime state
monitored[] = real monitored modules
telemetry   = uptime/load/health/architecture/last_event

IMPORTANT:
This file is TEST ONLY.
It does not create runtime truth.
It does not invent modules.
It does not calculate fake telemetry.
============================================================
*/

const TRUTH_API = "/api/test/status";


function text(element, value) {
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


function statusText(item) {
    if (!item) {
        return "N/A";
    }

    return item.status || "N/A";
}


/*
------------------------------------------------------------
RUNTIME
------------------------------------------------------------
Runtime is operational state.

It is NOT the monitored-module list.
*/
function renderRuntime(runtime) {

    if (!Array.isArray(runtime)) {
        return;
    }

    const byKey = {};

    runtime.forEach(item => {
        if (item && item.key) {
            byKey[item.key] = item;
        }
    });

    text(
        document.getElementById("test-ai-status"),
        statusText(byKey["brain_online"])
    );

    text(
        document.getElementById("test-builder-status"),
        statusText(byKey["builder_online"])
    );

    text(
        document.getElementById("test-automation-status"),
        statusText(byKey["automation_online"])
    );

    /*
     * Runtime health projection.
     */
    text(
        document.getElementById("health-kernel"),
        statusText(byKey["running"])
    );

    text(
        document.getElementById("health-ai"),
        statusText(byKey["brain_online"])
    );

    text(
        document.getElementById("health-data"),
        statusText(byKey["dashboard_online"])
    );
}


/*
------------------------------------------------------------
REAL MONITORED MODULES
------------------------------------------------------------

Only these API records are allowed here:

repository
generator
validation

Telemetry records such as "metrics" and "health" are never
treated as modules.
*/
function renderMonitored(monitored) {

    if (!Array.isArray(monitored)) {
        return;
    }

    const allowed = [
        "repository",
        "generator",
        "validation"
    ];

    const rows = monitored.filter(
        item =>
            item &&
            allowed.includes(item.key)
    );

    /*
     * Existing TEST design already contains module rows.
     * Reuse them instead of creating another UI structure.
     */
    const modules = Array.from(
        document.querySelectorAll(
            '.module[data-truth-module="true"]'
        )
    );

    rows.forEach((item, index) => {

        const row = modules[index];

        if (!row) {
            return;
        }

        const name =
            row.querySelector(
                '[data-truth-name="true"]'
            );

        /*
         * Existing module status is normally the first <b>.
         */
        const status =
            row.querySelector("b");

        const displayNames = {
            repository: "Repository",
            generator: "Generator",
            validation: "Validation"
        };

        text(
            name,
            displayNames[item.key] || item.name
        );

        text(
            status,
            statusText(item)
        );

        row.dataset.truthProjected = "true";
    });
}


/*
------------------------------------------------------------
TELEMETRY
------------------------------------------------------------
*/
function renderTelemetry(data) {

    if (!data) {
        return;
    }

    text(
        document.getElementById("uptime"),
        data.uptime
    );

    text(
        document.getElementById("load"),
        data.load === null ||
        data.load === undefined
            ? "N/A"
            : `${data.load}%`
    );

    text(
        document.getElementById("architecture"),
        data.architecture === null ||
        data.architecture === undefined
            ? "N/A"
            : `${data.architecture}%`
    );

    text(
        document.getElementById("last-event"),
        data.last_event
    );
}


/*
------------------------------------------------------------
CLOCK
------------------------------------------------------------
*/
function renderTimestamp(timestamp) {

    const candidates = [
        document.getElementById("timestamp"),
        document.getElementById("system-time"),
        document.querySelector("[data-truth-time]")
    ];

    const target =
        candidates.find(Boolean);

    if (!target || !timestamp) {
        return;
    }

    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
        text(target, timestamp);
        return;
    }

    text(
        target,
        date.toLocaleString()
    );
}


/*
------------------------------------------------------------
CANONICAL FETCH
------------------------------------------------------------
*/
async function updateTruth() {

    try {

        const url =
            `${TRUTH_API}?live=${Date.now()}`;

        const response =
            await fetch(
                url,
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
         * Canonical projections.
         */
        renderRuntime(data.runtime);
        renderMonitored(data.monitored);
        renderTelemetry(data);
        renderTimestamp(data.timestamp);

        /*
         * Mark dashboard as truth-connected.
         */
        document.documentElement.dataset.truthConnected =
            "true";

        document.documentElement.dataset.truthTimestamp =
            data.timestamp || "";

    }
    catch (error) {

        console.error(
            "FIOS Truth API error:",
            error
        );

        document.documentElement.dataset.truthConnected =
            "false";
    }
}


/*
------------------------------------------------------------
START
------------------------------------------------------------
*/
updateTruth();

/*
 * Live dashboard polling.
 * The server remains the source of truth.
 */
setInterval(
    updateTruth,
    2000
);