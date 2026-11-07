/* ====================================================================
   CTICD - Cyber Threat Intelligence Correlation Dashboard
   Real-Time SOC Telemetry, Threat Map & Intercept Dossier
   ==================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    initClocks();
    initSidebar();
    initCharts();
    initLiveTelemetryStream();
    initClipboardCopy();
});

// Global state for live attacks
window.CTICD_STATE = {
    audioEnabled: false,
    streamPaused: false,
    activeFilter: "all",
    recentAttacks: []
};

// ================= INDIAN STANDARD TIME (IST) CLOCKS =================

function initClocks() {
    const clockIst = document.getElementById("clockIst") || document.getElementById("clockUtc");
    const clockLocal = document.getElementById("clockLocal");
    const systemTime = document.getElementById("systemTime");

    function updateClocks() {
        const now = new Date();
        const istFormatter = new Intl.DateTimeFormat("en-IN", {
            timeZone: "Asia/Kolkata",
            hour12: false,
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        });
        const istTime = istFormatter.format(now);

        if (clockIst) {
            clockIst.textContent = `${istTime} IST`;
        }
        if (clockLocal) {
            clockLocal.textContent = `${istTime} IST`;
        }
        if (systemTime) {
            systemTime.textContent = `${istTime} IST`;
        }
    }

    updateClocks();
    setInterval(updateClocks, 1000);
}

// ================= RESPONSIVE SIDEBAR =================

function initSidebar() {
    const toggleBtn = document.getElementById("sidebarToggleBtn");
    const sidebar = document.getElementById("masterSidebar");

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            sidebar.classList.toggle("show-sidebar");
        });

        document.addEventListener("click", function (e) {
            if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                sidebar.classList.remove("show-sidebar");
            }
        });
    }
}

// ================= RADAR AUDIO SYNTHESIZER =================

function playTacticalPing(level) {
    if (!window.CTICD_STATE.audioEnabled) return;
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        const freq = level === "critical" ? 950 : 720;
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 1.5, ctx.currentTime + 0.08);

        gain.gain.setValueAtTime(0.06, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start();
        osc.stop(ctx.currentTime + 0.09);
    } catch (e) {
        // AudioContext policy
    }
}

window.toggleRadarAudio = function (btn) {
    window.CTICD_STATE.audioEnabled = !window.CTICD_STATE.audioEnabled;
    if (window.CTICD_STATE.audioEnabled) {
        btn.classList.add("active");
        btn.innerHTML = '<i class="bi bi-volume-up-fill text-info"></i> Audio Active';
        playTacticalPing("critical");
    } else {
        btn.classList.remove("active");
        btn.innerHTML = '<i class="bi bi-volume-mute"></i> Audio Muted';
    }
};

window.toggleStreamPause = function (btn) {
    window.CTICD_STATE.streamPaused = !window.CTICD_STATE.streamPaused;
    if (window.CTICD_STATE.streamPaused) {
        btn.classList.add("btn-warning");
        btn.innerHTML = '<i class="bi bi-play-fill"></i> Resume Stream';
    } else {
        btn.classList.remove("btn-warning");
        btn.innerHTML = '<i class="bi bi-pause-fill"></i> Pause Stream';
    }
};

// ================= CHARTS =================

function initCharts() {
    if (typeof Chart === "undefined") return;

    Chart.defaults.color = "#94a3b8";
    Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';

    const originCanvas = document.getElementById("originChart");
    if (originCanvas) {
        new Chart(originCanvas, {
            type: "doughnut",
            data: {
                labels: ["Russia", "China", "United States", "North Korea", "Netherlands", "Others"],
                datasets: [{
                    data: [31.5, 27.2, 16.4, 11.8, 7.3, 5.8],
                    backgroundColor: ["#ef4444", "#f97316", "#0ea5e9", "#a855f7", "#eab308", "#64748b"],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { boxWidth: 10, padding: 12, font: { size: 11 } }
                    }
                }
            }
        });
    }

    const typeCanvas = document.getElementById("typeChart");
    if (typeCanvas) {
        new Chart(typeCanvas, {
            type: "doughnut",
            data: {
                labels: ["C2 Beaconing", "Ransomware Exfil", "Edge Zero-Day", "DDoS Floods", "Credential Spray"],
                datasets: [{
                    data: [32.0, 24.5, 21.0, 13.5, 9.0],
                    backgroundColor: ["#ef4444", "#a855f7", "#f59e0b", "#0ea5e9", "#22c55e"],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { boxWidth: 10, padding: 12, font: { size: 11 } }
                    }
                }
            }
        });
    }

    const lineCanvas = document.getElementById("lineChart");
    if (lineCanvas) {
        const ctx = lineCanvas.getContext("2d");
        const gradient = ctx.createLinearGradient(0, 0, 0, 200);
        gradient.addColorStop(0, "rgba(14, 165, 233, 0.45)");
        gradient.addColorStop(1, "rgba(14, 165, 233, 0.0)");

        new Chart(lineCanvas, {
            type: "line",
            data: {
                labels: ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "Now"],
                datasets: [{
                    label: "Attack Velocity Index",
                    data: [68, 82, 65, 94, 88, 96, 91],
                    borderColor: "#0ea5e9",
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.4,
                    borderWidth: 2,
                    pointBackgroundColor: "#0ea5e9",
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { color: "rgba(148, 163, 184, 0.08)" } },
                    y: { grid: { color: "rgba(148, 163, 184, 0.08)" }, min: 50, max: 100 }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
}

// ================= REAL-TIME MAP & STREAM ENGINE =================

function initLiveTelemetryStream() {
    const mapContainer = document.getElementById("realCyberMap");
    let map = null;

    let activeMarkers = [];
    let activeLayers = [];
    let activeSources = [];

    if (mapContainer && typeof maplibregl !== "undefined") {
        if (mapContainer.dataset.initialized !== "true") {
            mapContainer.dataset.initialized = "true";

            const mapKey = window.MAP_KEY || "W1PfRLWxoIp2KSumhRV8";
            map = new maplibregl.Map({
                container: "realCyberMap",
                style: `https://api.maptiler.com/maps/dataviz-dark/style.json?key=${mapKey}`,
                center: [22, 24],
                zoom: 1.45,
                attributionControl: false
            });

            map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-left");
        }
    }

    function clearMapLayers() {
        if (!map) return;
        activeMarkers.forEach(m => m.remove());
        activeMarkers = [];
        activeLayers.forEach(l => { if (map.getLayer(l)) map.removeLayer(l); });
        activeSources.forEach(s => { if (map.getSource(s)) map.removeSource(s); });
        activeLayers = [];
        activeSources = [];
    }

    function createCurve(start, end) {
        const points = [];
        const count = 100;
        const dist = Math.sqrt(Math.pow(end[0] - start[0], 2) + Math.pow(end[1] - start[1], 2));
        const height = Math.min(22, Math.max(6, dist / 7.5));

        for (let i = 0; i <= count; i++) {
            const t = i / count;
            const lng = start[0] + (end[0] - start[0]) * t;
            const lat = start[1] + (end[1] - start[1]) * t + Math.sin(Math.PI * t) * height;
            points.push([lng, lat]);
        }
        return points;
    }

    function renderAttackOnMap(data) {
        if (!map || !map.isStyleLoaded()) return;

        const src = data.source;
        const tgt = data.target;
        const atk = data.attack;

        clearMapLayers();

        const curvePoints = createCurve([src.lng, src.lat], [tgt.lng, tgt.lat]);
        const lineId = "line-" + Date.now();
        const srcId = "src-" + Date.now();

        map.addSource(srcId, {
            type: "geojson",
            data: { type: "Feature", geometry: { type: "LineString", coordinates: curvePoints } }
        });

        map.addLayer({
            id: lineId,
            type: "line",
            source: srcId,
            layout: { "line-join": "round", "line-cap": "round" },
            paint: {
                "line-color": atk.color,
                "line-width": 2.8,
                "line-opacity": 0.9
            }
        });

        activeSources.push(srcId);
        activeLayers.push(lineId);

        // Origin Marker (Cyan pulse)
        const srcEl = document.createElement("div");
        srcEl.style.cssText = `width:12px;height:12px;background:#38bdf8;border-radius:50%;box-shadow:0 0 12px #38bdf8;cursor:pointer;`;
        srcEl.title = `Origin: ${src.city}, ${src.country} (${src.ip})`;
        srcEl.onclick = () => window.openTacticalDossier(data);
        const srcMarker = new maplibregl.Marker({ element: srcEl }).setLngLat([src.lng, src.lat]).addTo(map);
        activeMarkers.push(srcMarker);

        // Target Marker (Pulsing ring at destination)
        const tgtEl = document.createElement("div");
        tgtEl.style.cssText = `width:16px;height:16px;background:${atk.color};border-radius:50%;box-shadow:0 0 18px ${atk.color};border:2px solid #ffffff;cursor:pointer;`;
        tgtEl.title = `Target: ${tgt.organization} (${tgt.city}, ${tgt.country})`;
        tgtEl.onclick = () => window.openTacticalDossier(data);
        const tgtMarker = new maplibregl.Marker({ element: tgtEl }).setLngLat([tgt.lng, tgt.lat]).addTo(map);
        activeMarkers.push(tgtMarker);
    }

    function updateHud(data) {
        const liveFrom = document.getElementById("liveFrom");
        const liveTo = document.getElementById("liveTo");
        const liveType = document.getElementById("liveType");
        const liveTime = document.getElementById("liveTime");
        const liveMitre = document.getElementById("liveMitre");
        const liveBandwidth = document.getElementById("liveBandwidth");

        if (liveFrom) {
            liveFrom.innerHTML = `${data.source.flag} <b>${data.source.city}, ${data.source.country}</b> <span class="font-monospace text-info small">(${data.source.ip})</span>`;
        }
        if (liveTo) {
            liveTo.innerHTML = `${data.target.flag} <b>${data.target.city}, ${data.target.country}</b> <span class="text-warning small">[${data.target.organization}]</span>`;
        }
        if (liveType) {
            liveType.innerHTML = `<span style="color:${data.attack.color};font-weight:700;">${data.attack.type}</span> <span class="badge bg-dark border border-secondary text-light small">${data.attack.protocol}/${data.target.port}</span>`;
        }
        if (liveMitre) {
            liveMitre.innerHTML = `<span class="badge bg-info text-dark">${data.mitre.id}</span> ${data.mitre.name}`;
        }
        if (liveTime) {
            liveTime.textContent = (data.timestamp_time || "--:--:--") + " IST";
        }
        if (liveBandwidth) {
            liveBandwidth.textContent = `${data.telemetry.bandwidth} | ${data.telemetry.packets_per_sec}`;
        }
    }

    function appendToTerminal(data) {
        const terminalBody = document.getElementById("tacticalStreamBody") || document.getElementById("alertList");
        if (!terminalBody) return;

        // Store in global memory for modal lookup
        window.CTICD_STATE.recentAttacks.unshift(data);
        if (window.CTICD_STATE.recentAttacks.length > 50) {
            window.CTICD_STATE.recentAttacks.pop();
        }

        const row = document.createElement("div");
        row.className = `attack-row-item ${data.attack.level}`;
        row.dataset.eventId = data.event_id;
        row.onclick = () => window.openTacticalDossier(data);

        row.innerHTML = `
            <div class="d-flex align-items-center justify-content-between mb-1">
                <div class="d-flex align-items-center gap-2">
                    <span class="badge ${data.attack.level === 'critical' ? 'bg-danger' : 'bg-warning text-dark'}" style="font-size:10px;">
                        ${data.attack.level.toUpperCase()}
                    </span>
                    <strong class="text-white small">${data.attack.type}</strong>
                </div>
                <span class="font-monospace small text-info fw-bold" style="font-size:10px;">${data.timestamp_time} IST</span>
            </div>
            <div class="d-flex align-items-center justify-content-between text-secondary small" style="font-size:11.5px;">
                <span>
                    ${data.source.flag} ${data.source.city} <i class="bi bi-arrow-right text-info"></i> ${data.target.flag} ${data.target.city}
                    <span class="text-muted">(${data.target.sector.split(' ')[0]})</span>
                </span>
                <span class="badge bg-dark border border-secondary text-info font-monospace">${data.mitre.id}</span>
            </div>
        `;

        terminalBody.prepend(row);

        // Keep maximum 25 items in DOM to prevent lag
        while (terminalBody.children.length > 25) {
            terminalBody.removeChild(terminalBody.lastChild);
        }

        // Increment live counter
        const liveCounter = document.getElementById("liveAttackCount");
        if (liveCounter) {
            let val = parseInt(liveCounter.textContent.replace(/,/g, "")) || 4210;
            liveCounter.textContent = (val + 1).toLocaleString();
        }
    }

    window.setMapVectorFilter = function (filter, btn) {
        window.CTICD_STATE.activeFilter = filter;
        if (typeof playUiClick === "function") playUiClick();
        if (btn && btn.parentElement) {
            btn.parentElement.querySelectorAll("button").forEach(b => b.classList.remove("active", "border-info", "border-danger", "border-warning", "border-success"));
            btn.classList.add("active");
            if (filter === "critical") btn.classList.add("border-danger");
            else if (filter === "exploit") btn.classList.add("border-warning");
            else if (filter === "auth") btn.classList.add("border-success");
            else btn.classList.add("border-info");
        }
    };

    async function streamTick() {
        if (window.CTICD_STATE.streamPaused) return;

        try {
            const resp = await fetch("/api/live-attack");
            if (resp.ok) {
                const data = await resp.json();
                const filter = window.CTICD_STATE.activeFilter || "all";
                const atkType = (data.attack.type || "").toLowerCase();
                const atkCat = (data.attack.category || "").toLowerCase();

                const matches = filter === "all" ||
                    (filter === "critical" && data.attack.level === "critical") ||
                    (filter === "exploit" && (atkCat.includes("exploit") || atkType.includes("exploit") || atkType.includes("rce"))) ||
                    (filter === "ddos" && (atkType.includes("ddos") || atkCat.includes("ddos") || atkCat.includes("flood"))) ||
                    (filter === "auth" && (atkCat.includes("auth") || atkType.includes("auth") || atkType.includes("bypass")));

                if (matches) {
                    renderAttackOnMap(data);
                    updateHud(data);
                    appendToTerminal(data);
                    playTacticalPing(data.attack.level);
                }
            }
        } catch (err) {
            console.error("Telemetry stream sync error:", err);
        }
    }

    if (map) {
        map.on("load", function () {
            streamTick();
            setInterval(streamTick, 2800);
        });
    } else {
        setInterval(streamTick, 3000);
    }
}

// ================= TACTICAL INTERCEPT DOSSIER MODAL =================

window.openTacticalDossier = function (data) {
    if (!data) return;

    let modalEl = document.getElementById("tacticalDossierModal");
    if (!modalEl) {
        modalEl = createDossierModal();
    }

    document.getElementById("tdEventId").textContent = data.event_id;
    document.getElementById("tdTimestamp").textContent = data.timestamp_ist || (data.timestamp_time + " IST");
    document.getElementById("tdSeverity").textContent = data.attack.level.toUpperCase();
    document.getElementById("tdSeverity").className = `badge ${data.attack.level === 'critical' ? 'bg-danger' : 'bg-warning text-dark'} px-3 py-2`;
    document.getElementById("tdAttackType").textContent = data.attack.type;

    // Origin Telemetry
    document.getElementById("tdSrcLocation").innerHTML = `${data.source.flag} ${data.source.city}, ${data.source.country} (${data.source.continent})`;
    document.getElementById("tdSrcIp").textContent = `${data.source.ip}:${data.source.port}`;
    document.getElementById("tdSrcAsn").textContent = `${data.source.asn} (${data.source.isp})`;
    document.getElementById("tdSrcHost").textContent = data.source.hosting_type;
    document.getElementById("tdActor").textContent = data.source.threat_actor;
    document.getElementById("tdSrcCoords").textContent = `${data.source.lat}, ${data.source.lng}`;

    // Target Telemetry
    document.getElementById("tdTgtLocation").innerHTML = `${data.target.flag} ${data.target.city}, ${data.target.country}`;
    document.getElementById("tdTgtOrg").textContent = data.target.organization;
    document.getElementById("tdTgtSector").textContent = data.target.sector;
    document.getElementById("tdTgtAsset").textContent = data.target.asset_type;
    document.getElementById("tdTgtIp").textContent = `${data.target.ip}:${data.target.port} (${data.attack.protocol})`;

    // Frameworks & Telemetry
    document.getElementById("tdMitre").innerHTML = `<span class="badge bg-info text-dark">${data.mitre.id}</span> ${data.mitre.name} [Tactic: ${data.mitre.tactic}]`;
    document.getElementById("tdCve").innerHTML = `${data.cve.id} <span class="badge bg-danger ms-2">${data.cve.status}</span>`;
    document.getElementById("tdThroughput").textContent = `${data.telemetry.bandwidth} | ${data.telemetry.packets_per_sec}`;
    document.getElementById("tdVolume").textContent = `${data.telemetry.bytes_transferred} transferred (${data.telemetry.duration})`;
    document.getElementById("tdAction").textContent = data.attack.action_taken;
    document.getElementById("tdHex").textContent = data.attack.raw_hex_preview;
    document.getElementById("tdFwCmd").textContent = data.telemetry.fw_rule;

    // Set correlate link
    const corrBtn = document.getElementById("tdCorrelateBtn");
    if (corrBtn) {
        corrBtn.href = `/correlation-engine?indicator=${encodeURIComponent(data.source.ip)}`;
    }

    const modal = new bootstrap.Modal(modalEl);
    modal.show();
};

function createDossierModal() {
    const div = document.createElement("div");
    div.id = "tacticalDossierModal";
    div.className = "modal fade";
    div.tabIndex = -1;
    div.innerHTML = `
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content bg-dark text-light border border-info border-opacity-50" style="background:#030816 !important;">
            <div class="modal-header border-secondary border-opacity-25" style="background: rgba(15, 23, 42, 0.9);">
                <div>
                    <span class="badge bg-dark border border-secondary text-info font-monospace" id="tdEventId">EVT</span>
                    <h5 class="modal-title h6 fw-bold text-white mt-1" id="tdAttackType">Attack Telemetry</h5>
                    <small class="text-muted font-monospace" id="tdTimestamp">Timestamp</small>
                </div>
                <span id="tdSeverity" class="badge bg-danger">CRITICAL</span>
            </div>
            <div class="modal-body p-4">
                <!-- Source vs Target Row -->
                <div class="row g-3 mb-4">
                    <div class="col-md-6">
                        <div class="p-3 rounded bg-black border border-secondary border-opacity-25 h-100">
                            <h6 class="text-danger small text-uppercase fw-bold mb-2"><i class="bi bi-geo-alt"></i> Adversary Origin</h6>
                            <table class="table table-dark table-sm mb-0" style="font-size:12px;">
                                <tr><th width="110">Location:</th><td id="tdSrcLocation">-</td></tr>
                                <tr><th>Source IP:</th><td id="tdSrcIp" class="font-monospace text-info">-</td></tr>
                                <tr><th>ASN / ISP:</th><td id="tdSrcAsn" class="small">-</td></tr>
                                <tr><th>Host Type:</th><td id="tdSrcHost" class="text-warning">-</td></tr>
                                <tr><th>Attribution:</th><td id="tdActor" class="text-danger fw-bold">-</td></tr>
                                <tr><th>Coordinates:</th><td id="tdSrcCoords" class="font-monospace small text-muted">-</td></tr>
                            </table>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 rounded bg-black border border-secondary border-opacity-25 h-100">
                            <h6 class="text-success small text-uppercase fw-bold mb-2"><i class="bi bi-bullseye"></i> Targeted Asset</h6>
                            <table class="table table-dark table-sm mb-0" style="font-size:12px;">
                                <tr><th width="110">Location:</th><td id="tdTgtLocation">-</td></tr>
                                <tr><th>Organization:</th><td id="tdTgtOrg" class="fw-bold text-white">-</td></tr>
                                <tr><th>Industry Sector:</th><td id="tdTgtSector" class="text-info">-</td></tr>
                                <tr><th>Target Asset:</th><td id="tdTgtAsset" class="text-warning">-</td></tr>
                                <tr><th>Target Address:</th><td id="tdTgtIp" class="font-monospace">-</td></tr>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Technical TTPs & Exploits -->
                <h6 class="text-info small text-uppercase fw-bold mb-2"><i class="bi bi-shield-slash"></i> Technical Vector & Forensics</h6>
                <div class="p-3 rounded bg-black border border-secondary border-opacity-25 mb-3">
                    <table class="table table-dark table-sm mb-0" style="font-size:12px;">
                        <tr><th width="140">MITRE ATT&CK:</th><td id="tdMitre">-</td></tr>
                        <tr><th>Exploited CVE:</th><td id="tdCve">-</td></tr>
                        <tr><th>Throughput:</th><td id="tdThroughput" class="font-monospace text-warning">-</td></tr>
                        <tr><th>Traffic Metrics:</th><td id="tdVolume">-</td></tr>
                        <tr><th>SOC Action:</th><td id="tdAction" class="text-success fw-bold">-</td></tr>
                    </table>
                </div>

                <!-- Raw Packet Hex Dump -->
                <h6 class="text-info small text-uppercase fw-bold mb-2"><i class="bi bi-file-earmark-binary"></i> Forensic Packet Byte Preview</h6>
                <div class="hex-dump-container mb-3" id="tdHex">--</div>

                <!-- Perimeter Mitigation Rule -->
                <h6 class="text-info small text-uppercase fw-bold mb-2"><i class="bi bi-terminal"></i> Immediate Perimeter Mitigation</h6>
                <div class="code-box">
                    <button class="code-copy-btn" onclick="copyCode(this, 'tdFwCmd')"><i class="bi bi-clipboard"></i> Copy</button>
                    <code id="tdFwCmd">--</code>
                </div>
            </div>
            <div class="modal-footer border-secondary border-opacity-25" style="background: rgba(15, 23, 42, 0.9);">
                <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Close Dossier</button>
                <a href="#" id="tdCorrelateBtn" class="btn cyber-btn btn-sm">
                    <i class="bi bi-diagram-3"></i> Open in Correlation Graph
                </a>
            </div>
        </div>
    </div>
    `;
    document.body.appendChild(div);
    return div;
}

// ================= CLIPBOARD UTILITY =================

function initClipboardCopy() {
    window.copyCode = function (btn, elementId) {
        const target = document.getElementById(elementId);
        if (!target) return;
        const text = target.textContent || target.innerText;
        navigator.clipboard.writeText(text).then(() => {
            const orig = btn.innerHTML;
            btn.innerHTML = '<i class="bi bi-check2"></i> Copied!';
            btn.classList.add("text-success");
            setTimeout(() => {
                btn.innerHTML = orig;
                btn.classList.remove("text-success");
            }, 2000);
        });
    };
}


// ====================================================================
// ADVANCED IMMERSIVE FEATURES: THEMES, DEFCON, COMMAND PALETTE,
// AI COPILOT, AUDIO SYNTHESIZER & KEYBOARD NAVIGATION
// ====================================================================

document.addEventListener("DOMContentLoaded", function () {
    initImmersiveFeatures();
});

function initImmersiveFeatures() {
    // 1. Theme Restorer
    const savedTheme = localStorage.getItem("cticd_theme") || "cyan";
    setTheme(savedTheme, false);

    // 2. DEFCON Restorer
    const savedDefcon = localStorage.getItem("cticd_defcon") || "2";
    setDefcon(savedDefcon, false);

    // 3. Audio Restorer
    const savedAudio = localStorage.getItem("cticd_audio") === "true";
    window.CTICD_STATE.audioEnabled = savedAudio;
    updateAudioButtonsUi(savedAudio);

    // 4. War Room HUD Restorer
    const savedWarRoom = localStorage.getItem("cticd_war_room") === "true";
    if (savedWarRoom) {
        document.body.classList.add("war-room-mode");
    }

    // 5. Command Palette Setup
    initCommandPalette();

    // 6. AI Copilot Setup
    initAiCopilot();

    // 7. Global Keyboard Shortcuts
    initKeyboardShortcuts();
}

// --- Audio FX Synthesizer (Web Audio API) ---
function getAudioContext() {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return null;
    if (!window._cticdAudioCtx) {
        window._cticdAudioCtx = new AudioContext();
    }
    if (window._cticdAudioCtx.state === "suspended") {
        window._cticdAudioCtx.resume();
    }
    return window._cticdAudioCtx;
}

function playUiClick() {
    if (!window.CTICD_STATE.audioEnabled) return;
    try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(1400, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(800, ctx.currentTime + 0.03);
        gain.gain.setValueAtTime(0.04, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.03);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.035);
    } catch (e) {}
}

function playDefconAlarm() {
    if (!window.CTICD_STATE.audioEnabled) return;
    try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.setValueAtTime(880, now + 0.1);
        osc.frequency.setValueAtTime(440, now + 0.2);
        osc.frequency.setValueAtTime(880, now + 0.3);
        gain.gain.setValueAtTime(0.06, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.42);
    } catch (e) {}
}

function playSuccessChime() {
    if (!window.CTICD_STATE.audioEnabled) return;
    try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = "triangle";
            osc.frequency.setValueAtTime(freq, now + i * 0.06);
            gain.gain.setValueAtTime(0.04, now + i * 0.06);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.06 + 0.12);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + i * 0.06);
            osc.stop(now + i * 0.06 + 0.13);
        });
    } catch (e) {}
}

function updateAudioButtonsUi(enabled) {
    document.querySelectorAll(".radar-audio-btn, #topbarAudioBtn").forEach(btn => {
        if (enabled) {
            btn.innerHTML = '<i class="bi bi-volume-up-fill text-success"></i> Audio Active';
            btn.classList.add("text-success");
        } else {
            btn.innerHTML = '<i class="bi bi-volume-mute"></i> Audio Muted';
            btn.classList.remove("text-success");
        }
    });
}

window.toggleAudioFx = function () {
    window.CTICD_STATE.audioEnabled = !window.CTICD_STATE.audioEnabled;
    localStorage.setItem("cticd_audio", window.CTICD_STATE.audioEnabled);
    updateAudioButtonsUi(window.CTICD_STATE.audioEnabled);
    if (window.CTICD_STATE.audioEnabled) {
        playSuccessChime();
    }
};

// --- Theme Selector ---
window.setTheme = function (themeName, playSound = true) {
    document.documentElement.setAttribute("data-theme", themeName);
    localStorage.setItem("cticd_theme", themeName);
    if (playSound) playUiClick();
};

// --- DEFCON Level Controller ---
window.setDefcon = function (level, playSound = true) {
    level = String(level);
    document.body.classList.remove("defcon-1", "defcon-2", "defcon-3", "defcon-4", "defcon-5");
    document.body.classList.add(`defcon-${level}`);
    localStorage.setItem("cticd_defcon", level);

    const labels = {
        "1": "DEFCON 1 / MAXIMUM ALERT",
        "2": "DEFCON 2 / ELEVATED",
        "3": "DEFCON 3 / TACTICAL WATCH",
        "4": "DEFCON 4 / GUARDED",
        "5": "DEFCON 5 / NORMAL DEFENSE"
    };

    const colors = {
        "1": "#ef4444",
        "2": "#f97316",
        "3": "#eab308",
        "4": "#0ea5e9",
        "5": "#22c55e"
    };

    const labelSpan = document.getElementById("topbarDefconLabel");
    const dotSpan = document.getElementById("topbarDefconDot");
    if (labelSpan) labelSpan.textContent = labels[level] || `DEFCON ${level}`;
    if (dotSpan) {
        dotSpan.style.background = colors[level] || "#ef4444";
        dotSpan.style.boxShadow = `0 0 10px ${colors[level] || "#ef4444"}`;
    }

    if (playSound) {
        if (level === "1" || level === "2") {
            playDefconAlarm();
        } else {
            playUiClick();
        }
    }
};

// --- War Room HUD Mode Toggle ---
window.toggleWarRoomMode = function () {
    const isWarRoom = document.body.classList.toggle("war-room-mode");
    localStorage.setItem("cticd_war_room", isWarRoom);
    playUiClick();
};

// --- Command Palette Engine ---
function initCommandPalette() {
    const backdrop = document.getElementById("commandPaletteBackdrop");
    const input = document.getElementById("commandPaletteInput");
    const list = document.getElementById("commandPaletteList");
    if (!backdrop || !input || !list) return;

    // Attach Ctrl+K trigger badge if present
    document.querySelectorAll(".search-kbd-badge").forEach(badge => {
        badge.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            openCommandPalette();
        });
    });

    window.openCommandPalette = function (initialQuery = "") {
        backdrop.classList.add("active");
        input.value = initialQuery;
        input.focus();
        filterCommandPalette(initialQuery);
        playUiClick();
    };

    window.closeCommandPalette = function () {
        backdrop.classList.remove("active");
    };

    backdrop.addEventListener("click", function (e) {
        if (e.target === backdrop) closeCommandPalette();
    });

    input.addEventListener("input", function () {
        filterCommandPalette(input.value);
    });

    // Arrow navigation
    input.addEventListener("keydown", function (e) {
        const items = list.querySelectorAll(".cmd-palette-item:not([style*='display: none'])");
        if (!items.length) return;
        let currentIndex = -1;
        items.forEach((item, idx) => {
            if (item.classList.contains("active")) currentIndex = idx;
        });

        if (e.key === "ArrowDown") {
            e.preventDefault();
            const nextIdx = (currentIndex + 1) % items.length;
            items.forEach(i => i.classList.remove("active"));
            items[nextIdx].classList.add("active");
            items[nextIdx].scrollIntoView({ block: "nearest" });
            playUiClick();
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            const prevIdx = (currentIndex - 1 + items.length) % items.length;
            items.forEach(i => i.classList.remove("active"));
            items[prevIdx].classList.add("active");
            items[prevIdx].scrollIntoView({ block: "nearest" });
            playUiClick();
        } else if (e.key === "Enter") {
            e.preventDefault();
            const activeItem = items[currentIndex] || items[0];
            if (activeItem) {
                activeItem.click();
            } else if (input.value.trim()) {
                window.location.href = `/global-search?q=${encodeURIComponent(input.value.trim())}`;
            }
        } else if (e.key === "Escape") {
            closeCommandPalette();
        }
    });

    function filterCommandPalette(query) {
        query = query.toLowerCase().trim();
        const items = list.querySelectorAll(".cmd-palette-item");
        let first = true;
        items.forEach(item => {
            const text = (item.getAttribute("data-keywords") || item.innerText).toLowerCase();
            if (!query || text.includes(query)) {
                item.style.display = "flex";
                if (first) {
                    item.classList.add("active");
                    first = false;
                } else {
                    item.classList.remove("active");
                }
            } else {
                item.style.display = "none";
                item.classList.remove("active");
            }
        });
    }
}

// --- AI SOC Copilot Engine ---
function initAiCopilot() {
    const fab = document.getElementById("aiCopilotFab");
    const drawer = document.getElementById("aiCopilotDrawer");
    const input = document.getElementById("aiCopilotInput");
    const sendBtn = document.getElementById("aiCopilotSendBtn");
    const msgStream = document.getElementById("aiCopilotMessages");

    if (!drawer) return;

    window.toggleAiCopilot = function () {
        drawer.classList.toggle("open");
        if (drawer.classList.contains("open")) {
            playUiClick();
            if (input) input.focus();
        }
    };

    if (fab) fab.addEventListener("click", toggleAiCopilot);

    const closeBtn = document.getElementById("aiCopilotCloseBtn");
    if (closeBtn) closeBtn.addEventListener("click", toggleAiCopilot);

    window.sendCopilotPrompt = function (text) {
        if (!text || !text.trim()) return;
        playUiClick();
        if (!drawer.classList.contains("open")) drawer.classList.add("open");

        // User message
        appendCopilotMessage(text, "user");
        if (input) input.value = "";

        // Simulated AI response based on CTI intelligence knowledge base
        setTimeout(() => {
            generateCopilotResponse(text);
        }, 400);
    };

    if (sendBtn && input) {
        sendBtn.addEventListener("click", () => sendCopilotPrompt(input.value));
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") sendCopilotPrompt(input.value);
        });
    }

    function appendCopilotMessage(contentHtml, sender = "agent") {
        if (!msgStream) return;
        const msgDiv = document.createElement("div");
        msgDiv.className = `copilot-msg ${sender}`;

        const senderLabel = sender === "user" ? "You (Lead SOC Analyst)" : "CTICD AI Defense Copilot";
        const avatarIcon = sender === "user" ? "bi-person-fill" : "bi-cpu-fill text-info";

        msgDiv.innerHTML = `
            <div class="small text-muted d-flex align-items-center gap-1" style="font-size:10px;">
                <i class="bi ${avatarIcon}"></i> ${senderLabel}
            </div>
            <div class="copilot-bubble">${contentHtml}</div>
        `;
        msgStream.appendChild(msgDiv);
        msgStream.scrollTop = msgStream.scrollHeight;
    }

    function generateCopilotResponse(query) {
        query = query.toLowerCase();
        let reply = "";

        if (query.includes("defcon")) {
            const level = localStorage.getItem("cticd_defcon") || "2";
            reply = `
                <strong>Active Condition: DEFCON ${level}</strong><br>
                Under current telemetry, external probes against sovereign assets and telecommunication backbones are elevated.
                <ul class="mb-2 mt-2 ps-3">
                    <li>Perimeter firewall drop rate: <strong>99.8% containment</strong></li>
                    <li>Threat Actor Focus: <strong>Scattered Spider & Volt Typhoon</strong></li>
                    <li>Recommendation: Enforce Geo-IP fencing on port 2152 (5G UPF core) and rotate TLS session keys.</li>
                </ul>
            `;
        } else if (query.includes("apt29") || query.includes("cozy bear")) {
            reply = `
                <strong>Adversary Profile: APT29 (Cozy Bear / Midnight Blizzard)</strong><br>
                <div class="small text-info mt-1 font-monospace">Origin: SVR RF | Diamond Model: State-Sponsored Espionage</div>
                <div class="mt-2">Primary TTPs observed:</div>
                <ul class="mb-2 ps-3">
                    <li><span class="badge bg-danger">T1078</span> Valid Cloud Accounts & OAuth tokens</li>
                    <li><span class="badge bg-danger">T1071.001</span> Web Service C2 (M365 Graph API)</li>
                </ul>
                <div class="code-box p-2 mb-0" style="font-size:11px;">
                    <code>iptables -I INPUT -s 185.220.101.45 -j DROP</code>
                </div>
            `;
        } else if (query.includes("cve-2024-3094") || query.includes("xz")) {
            reply = `
                <strong>Vulnerability Brief: CVE-2024-3094 (XZ Utils Liblzma Backdoor)</strong><br>
                <span class="badge bg-danger">CVSS 10.0 CRITICAL</span> <span class="badge bg-warning text-dark">CISA KEV Enforced</span>
                <p class="mt-2 mb-2">Backdoor in upstream tarballs intercepting <code>RSA_public_decrypt</code> via <code>libsystemd</code> integration into OpenSSH.</p>
                <strong>Immediate Mitigation:</strong> Downgrade to XZ version <code>5.4.x</code> or upgrade to vendor-patched distributions immediately.
            `;
        } else if (query.includes("firewall") || query.includes("iptables") || query.includes("drop")) {
            reply = `
                <strong>Recommended Automated Perimeter Drop Rules:</strong><br>
                <div class="code-box p-2 mb-1" style="font-size:11px;">
                    <code>iptables -I INPUT -s 185.220.101.45 -p tcp --dport 443 -j DROP<br>iptables -I INPUT -s 45.144.227.55 -j DROP</code>
                </div>
                <small class="text-success"><i class="bi bi-shield-check"></i> Rules tested and formatted for Linux iptables, Cisco ASA, and Palo Alto PAN-OS.</small>
            `;
        } else if (query.includes("incident") || query.includes("mitigate") || query.includes("steps")) {
            reply = `
                <strong>Incident Response Triage Playbook:</strong><br>
                <ol class="ps-3 mb-1 mt-1 small">
                    <li><strong>Identify:</strong> Correlate suspicious IP in the <a href="/correlation-engine" class="text-info">Correlation Engine</a>.</li>
                    <li><strong>Isolate:</strong> Revoke active OAuth bearer tokens and isolate compromised endpoints.</li>
                    <li><strong>Eradicate:</strong> Block C2 IPs at perimeter WAF / Border Gateway Protocol (BGP).</li>
                    <li><strong>Export:</strong> Download the STIX 2.1 JSON bundle from <a href="/reports" class="text-info">Executive Reports</a> for CISO briefing.</li>
                </ol>
            `;
        } else {
            reply = `
                <strong>Intelligence Synthesis on: "${query}"</strong><br>
                Cross-referencing global telemetry databases...
                <p class="mt-2 mb-1">Our threat engine matches this indicator with active sensor nodes across 32 sovereign hubs. Review the real-time ballistic trajectories on the <a href="/threat-map" class="text-info">Threat Map</a> or run deep OSINT scanning in the <a href="/ioc-search" class="text-info">IOC Search</a>.</p>
            `;
        }

        appendCopilotMessage(reply, "agent");
        playSuccessChime();
    }
}

// --- Global Keyboard Shortcuts ---
function initKeyboardShortcuts() {
    let gPressed = false;
    let gTimeout = null;

    document.addEventListener("keydown", function (e) {
        // Do not trigger if typing in form inputs
        const tag = (e.target.tagName || "").toLowerCase();
        if (tag === "input" || tag === "textarea" || e.target.isContentEditable) {
            if (e.key === "Escape") {
                e.target.blur();
                const cmdBackdrop = document.getElementById("commandPaletteBackdrop");
                if (cmdBackdrop) cmdBackdrop.classList.remove("active");
                const drawer = document.getElementById("aiCopilotDrawer");
                if (drawer) drawer.classList.remove("open");
            }
            return;
        }

        // 1. Ctrl + K / Cmd + K -> Command Palette
        if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) {
            e.preventDefault();
            window.openCommandPalette();
            return;
        }

        // 2. / -> Quick Search Palette
        if (e.key === "/") {
            e.preventDefault();
            window.openCommandPalette();
            return;
        }

        // 3. Alt + C -> AI Copilot Drawer
        if (e.altKey && (e.key === "c" || e.key === "C")) {
            e.preventDefault();
            window.toggleAiCopilot();
            return;
        }

        // 4. Alt + M -> Toggle Audio
        if (e.altKey && (e.key === "m" || e.key === "M")) {
            e.preventDefault();
            window.toggleAudioFx();
            return;
        }

        // 5. Alt + W -> Toggle War Room HUD
        if (e.altKey && (e.key === "w" || e.key === "W")) {
            e.preventDefault();
            window.toggleWarRoomMode();
            return;
        }

        // 6. ? -> Keyboard Shortcuts Modal
        if (e.key === "?") {
            e.preventDefault();
            const modalEl = document.getElementById("shortcutsModal");
            if (modalEl) {
                const bsModal = new bootstrap.Modal(modalEl);
                bsModal.show();
                playUiClick();
            }
            return;
        }

        // 7. Escape -> Close modals and drawers
        if (e.key === "Escape") {
            const cmdBackdrop = document.getElementById("commandPaletteBackdrop");
            if (cmdBackdrop) cmdBackdrop.classList.remove("active");
            const drawer = document.getElementById("aiCopilotDrawer");
            if (drawer) drawer.classList.remove("open");
            return;
        }

        // 8. Multi-key Go (G + Key)
        if (e.key === "g" || e.key === "G") {
            gPressed = true;
            clearTimeout(gTimeout);
            gTimeout = setTimeout(() => { gPressed = false; }, 1000);
            return;
        }

        if (gPressed) {
            gPressed = false;
            const key = e.key.toLowerCase();
            const navMap = {
                "d": "/dashboard",
                "m": "/threat-map",
                "f": "/threat-feed",
                "i": "/ioc-search",
                "c": "/correlation-engine",
                "v": "/cve-explorer",
                "s": "/malware-analysis",
                "a": "/alerts",
                "r": "/reports",
                "p": "/profile"
            };
            if (navMap[key]) {
                e.preventDefault();
                playUiClick();
                window.location.href = navMap[key];
            }
        }
    });
}

// --- MITRE Technique Inspector Modal ---
window.inspectMitreTechnique = function (tactic, techId, techName, actor, rule) {
    playUiClick();
    let modalEl = document.getElementById("mitreTechniqueModal");
    if (!modalEl) {
        const div = document.createElement("div");
        div.className = "modal fade";
        div.id = "mitreTechniqueModal";
        div.tabIndex = -1;
        div.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content border border-info border-opacity-50" style="background:#0f172a; box-shadow:0 0 40px rgba(14,165,233,0.3);">
                <div class="modal-header border-secondary border-opacity-25">
                    <div>
                        <span class="badge bg-danger me-2" id="mitreModalId">T0000</span>
                        <strong class="text-white" id="mitreModalName">Technique Name</strong>
                    </div>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p class="text-muted small mb-2">Tactic Stage: <strong class="text-info" id="mitreModalTactic">Initial Access</strong></p>
                    <p class="text-muted small mb-3">Primary Threat Actor: <strong class="text-danger" id="mitreModalActor">APT29</strong></p>
                    <h6 class="text-info small fw-bold"><i class="bi bi-shield-check"></i> Recommended Detection Signature</h6>
                    <div class="code-box mb-0">
                        <code id="mitreModalRule">alert tcp any any -> any any (msg:"TTP Detection"; sid:1000001;)</code>
                    </div>
                </div>
                <div class="modal-footer border-secondary border-opacity-25">
                    <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Close</button>
                    <a href="#" id="mitreModalCorrelate" class="btn cyber-btn btn-sm">Correlate in Graph</a>
                </div>
            </div>
        </div>`;
        document.body.appendChild(div);
        modalEl = div;
    }

    document.getElementById("mitreModalId").textContent = techId;
    document.getElementById("mitreModalName").textContent = techName;
    document.getElementById("mitreModalTactic").textContent = tactic;
    document.getElementById("mitreModalActor").textContent = actor;
    document.getElementById("mitreModalRule").textContent = rule;
    document.getElementById("mitreModalCorrelate").href = `/correlation-engine?indicator=${encodeURIComponent(techId)}`;

    const bsModal = new bootstrap.Modal(modalEl);
    bsModal.show();
};
