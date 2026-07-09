window.addEventListener("load", function () {
    initCharts();
    initLiveMap();
});

function nowTime() {
    return new Date().toLocaleTimeString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });
}

function initCharts() {
    const origin = document.getElementById("originChart");
    const type = document.getElementById("typeChart");
    const line = document.getElementById("lineChart");

    if (typeof Chart === "undefined") {
        return;
    }

    if (origin) {
        new Chart(origin, {
            type: "doughnut",
            data: {
                labels: ["United States", "Russia", "China", "Germany", "Others"],
                datasets: [{
                    data: [24.3, 18.7, 15.2, 9.8, 32],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: "68%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#cbd5e1",
                            boxWidth: 10,
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }

    if (type) {
        new Chart(type, {
            type: "doughnut",
            data: {
                labels: ["Brute Force", "DDoS", "Malware", "SQL Injection", "Phishing"],
                datasets: [{
                    data: [28.7, 22.1, 17.3, 13.6, 18.3],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: "68%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#cbd5e1",
                            boxWidth: 10,
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }

    if (line) {
        new Chart(line, {
            type: "line",
            data: {
                labels: ["May 8", "May 9", "May 10", "May 11", "May 12", "May 13", "May 14"],
                datasets: [{
                    data: [58, 72, 52, 73, 53, 78, 90],
                    fill: true,
                    tension: 0.42,
                    borderWidth: 2,
                    pointRadius: 3
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(30,41,59,.8)" }
                    },
                    y: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(30,41,59,.8)" }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
}
function initLiveMap() {

    const mapContainer = document.getElementById("realCyberMap");

    if (!mapContainer || typeof maplibregl === "undefined") {
        return;
    }

    if (mapContainer.dataset.initialized === "true") {
        return;
    }

    mapContainer.dataset.initialized = "true";

    const map = new maplibregl.Map({
        container: "realCyberMap",

        style:
            `https://api.maptiler.com/maps/dataviz-dark/style.json?key=${window.MAP_KEY}`,

        center: [25, 20],
        zoom: 1.4,

        attributionControl: false
    });

    map.addControl(
        new maplibregl.NavigationControl(),
        "top-left"
    );

    let activeMarkers = [];
    let activeLayers = [];
    let activeSources = [];
    let activeTimers = [];
        function createCurve(start, end) {

        const points = [];

        const total = 120;

        const distance =
            Math.abs(end[0] - start[0]) +
            Math.abs(end[1] - start[1]);

        const height =
            Math.min(
                10,
                Math.max(
                    4,
                    distance / 15
                )
            );

        for (let i = 0; i <= total; i++) {

            const t = i / total;

            const lng =
                start[0] +
                (end[0] - start[0]) * t;

            const lat =
                start[1] +
                (end[1] - start[1]) * t +
                Math.sin(Math.PI * t) * height;

            points.push([lng, lat]);

        }

        return points;

    }
        function createMarker(type, level, city, label, ip) {

        const wrapper = document.createElement("div");

        wrapper.className = "fixed-marker-wrapper";

        wrapper.innerHTML = `

        <div class="attack-marker ${level}"></div>

        <div class="marker-tag">

            <b>${city}</b>

            <span>${label}</span>

            <small>${ip}</small>

        </div>

        `;

        return wrapper;

    }
        function clearAttack() {

        activeTimers.forEach(clearInterval);

        activeTimers = [];

        activeMarkers.forEach(marker => marker.remove());

        activeMarkers = [];

        activeLayers.forEach(layer => {

            if (map.getLayer(layer))
                map.removeLayer(layer);

        });

        activeSources.forEach(source => {

            if (map.getSource(source))
                map.removeSource(source);

        });

        activeLayers = [];

        activeSources = [];

    }
        async function fetchLiveAttack() {
        try {
            const response = await fetch("/api/live-attack");

            if (!response.ok) {
                throw new Error("Live attack API failed");
            }

            const data = await response.json();
            showAttack(data);

        } catch (error) {
            console.error("Live attack fetch error:", error);
        }
    }

    function updateLivePanel(data) {
        const source = data.source;
        const target = data.target;
        const attack = data.attack;

        const liveFrom = document.getElementById("liveFrom");
        const liveTo = document.getElementById("liveTo");
        const liveType = document.getElementById("liveType");
        const liveMitre = document.getElementById("liveMitre");
        const liveTime = document.getElementById("liveTime");
        const systemTime = document.getElementById("systemTime");

        if (liveFrom) {
            liveFrom.innerHTML = `
                ${source.country}
                <br>
                <small>${source.city} | ${source.ip}</small>
            `;
        }

        if (liveTo) {
            liveTo.innerHTML = `
                ${target.country}
                <br>
                <small>${target.city} | ${target.ip}</small>
            `;
        }

        if (liveType) {
            liveType.innerHTML = `
                ${attack.type}
                <br>
                <small>${attack.mitre_id} - ${attack.mitre_name}</small>
            `;
        }

        if (liveMitre) {
            liveMitre.innerText = `${attack.mitre_id} - ${attack.mitre_name}`;
        }

        if (liveTime) {
            liveTime.innerText = nowTime();
        }

        if (systemTime) {
            systemTime.innerText = nowTime();
        }
    }

    function updateStats(data) {
        const attack = data.attack;

        const liveAttackCount = document.getElementById("liveAttackCount");
        const maliciousIpCount = document.getElementById("maliciousIpCount");
        const iocCount = document.getElementById("iocCount");
        const countryCount = document.getElementById("countryCount");

        const mapLiveAttacks = document.getElementById("mapLiveAttacks");
        const mapCriticalCount = document.getElementById("mapCriticalCount");
        const mapCountryCount = document.getElementById("mapCountryCount");
        const mapTopTechnique = document.getElementById("mapTopTechnique");
        const mapRiskScore = document.getElementById("mapRiskScore");

        const liveValue = Number(data.packets || 0) || Math.floor(Math.random() * 700) + 1200;
        const maliciousValue = Math.floor(Math.random() * 1400) + 8400;
        const iocValue = Math.floor(Math.random() * 4000) + 22000;
        const countryValue = Math.floor(Math.random() * 25) + 120;
        const criticalValue = Math.floor(Math.random() * 30) + 40;
        const riskValue = Math.floor(Math.random() * 12) + 86;

        if (liveAttackCount) {
            liveAttackCount.innerText = liveValue.toLocaleString();
        }

        if (maliciousIpCount) {
            maliciousIpCount.innerText = maliciousValue;
        }

        if (iocCount) {
            iocCount.innerText = iocValue;
        }

        if (countryCount) {
            countryCount.innerText = countryValue;
        }

        if (mapLiveAttacks) {
            mapLiveAttacks.innerText = liveValue.toLocaleString();
        }

        if (mapCriticalCount) {
            mapCriticalCount.innerText =
                attack.level === "critical" ? criticalValue : Math.floor(criticalValue / 2);
        }

        if (mapCountryCount) {
            mapCountryCount.innerText = countryValue;
        }

        if (mapRiskScore) {
            mapRiskScore.innerText = riskValue;
        }

        if (mapTopTechnique) {
            mapTopTechnique.innerText = attack.mitre_id || "T1110";
        }
    }

    function updateAlertList(data) {
        const alertList = document.getElementById("alertList");

        if (!alertList) {
            return;
        }

        const source = data.source;
        const target = data.target;
        const attack = data.attack;

        const div = document.createElement("div");
        div.className = "alert-item";

        div.innerHTML = `
            <div class="dot ${attack.level}"></div>
            <div>
                <h5>${attack.type}</h5>
                <p>${source.country} (${source.ip}) → ${target.country} (${target.ip})</p>
            </div>
            <span>${nowTime()}</span>
        `;

        alertList.prepend(div);

        while (alertList.children.length > 6) {
            alertList.removeChild(alertList.lastElementChild);
        }
    }
        function showAttack(data) {
        clearAttack();

        const source = data.source;
        const target = data.target;
        const attack = data.attack;

        const fromCoord = [
            Number(source.lng),
            Number(source.lat)
        ];

        const toCoord = [
            Number(target.lng),
            Number(target.lat)
        ];

        const routeCoordinates = createCurve(fromCoord, toCoord);

        const routeSourceId = "live-route-source";
        const routeLayerId = "live-route-layer";
        const particleSourceId = "live-particle-source";
        const particleLayerId = "live-particle-layer";

        map.addSource(routeSourceId, {
            type: "geojson",
            data: {
                type: "Feature",
                geometry: {
                    type: "LineString",
                    coordinates: routeCoordinates
                }
            }
        });

        map.addLayer({
            id: routeLayerId,
            type: "line",
            source: routeSourceId,
            layout: {
                "line-cap": "round",
                "line-join": "round"
            },
            paint: {
                "line-color": attack.color,
                "line-width": 4,
                "line-opacity": 0.95,
                "line-dasharray": [2, 2]
            }
        });

        activeSources.push(routeSourceId);
        activeLayers.push(routeLayerId);

        map.addSource(particleSourceId, {
            type: "geojson",
            data: {
                type: "FeatureCollection",
                features: []
            }
        });

        map.addLayer({
            id: particleLayerId,
            type: "circle",
            source: particleSourceId,
            paint: {
                "circle-radius": 7,
                "circle-color": attack.color,
                "circle-blur": 0.35,
                "circle-opacity": 1
            }
        });

        activeSources.push(particleSourceId);
        activeLayers.push(particleLayerId);

        const sourceMarker = new maplibregl.Marker({
            element: createMarker(
                "source",
                attack.level,
                source.city + ", " + source.country,
                "LIVE SOURCE",
                source.ip
            ),
            anchor: "center",
            offset: [0, 0]
        })
            .setLngLat(fromCoord)
            .addTo(map);

        const targetMarker = new maplibregl.Marker({
            element: createMarker(
                "target",
                attack.level,
                target.city + ", " + target.country,
                "LIVE TARGET",
                target.ip
            ),
            anchor: "center",
            offset: [0, 0]
        })
            .setLngLat(toCoord)
            .addTo(map);

        activeMarkers.push(sourceMarker, targetMarker);

        let particleStep = 0;

        const particleTimer = setInterval(function () {
            if (!map.getSource(particleSourceId)) {
                clearInterval(particleTimer);
                return;
            }

            const point =
                routeCoordinates[particleStep % routeCoordinates.length];

            map.getSource(particleSourceId).setData({
                type: "FeatureCollection",
                features: [
                    {
                        type: "Feature",
                        geometry: {
                            type: "Point",
                            coordinates: point
                        }
                    }
                ]
            });

            particleStep += 2;
        }, 55);

        let dashStep = 0;

        const dashTimer = setInterval(function () {
            if (!map.getLayer(routeLayerId)) {
                clearInterval(dashTimer);
                return;
            }

            dashStep = (dashStep + 1) % 5;

            map.setPaintProperty(
                routeLayerId,
                "line-dasharray",
                [2, 2 + dashStep]
            );
        }, 350);

        activeTimers.push(particleTimer, dashTimer);

        updateLivePanel(data);
        updateStats(data);
        updateAlertList(data);
    }

    map.on("load", function () {
        fetchLiveAttack();

        setInterval(fetchLiveAttack, 5000);
    });
}