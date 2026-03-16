// Average carbon intensity of data transfer (grams of CO2 per GB streamed)
// This converts estimated data usage into emissions.
const CO2_PER_GB = 36;
const WATER_DC_KWH_PER_GB = 0.055;
const WUE_DC = 1.9;
const WATER_NETWORK_KWH_PER_GB = 0.059;
const WUE_NETWORK = 4.45;

// Estimated average streaming bitrates per resolution (in Mbps).
// These values allow us to approximate total data consumption.
const BITRATE_MAP = {
    "144p": 0.1,
    "240p": 0.3,
    "360p": 0.7,
    "480p": 1,
    "720p": 2.5,
    "1080p": 5,
    "1440p": 10,
    "2160p": 15,
    "4320p": 25
};

// Ordered list of resolutions from lowest to highest.
// Used to scale the bottle visualization proportionally.
const RES_ORDER = ["144p","240p","360p","480p","720p","1080p","1440p","2160p","4320p"];

// Returns the lowest available resolution (used as baseline impact).
function getMinResolution() {
    return RES_ORDER[0];
}

// Returns the highest available resolution (used as maximum impact).
function getMaxResolution() {
    return RES_ORDER[RES_ORDER.length-1];
}

// Tracks last detected resolution to prevent unnecessary recalculation.
let lastKnownResolution = null;

// Tracks current video ID to detect navigation changes.
let currentVideoId = null;

// Extracts video duration from YouTube player and converts it to seconds.
// This is required to estimate total streamed data.
function getDurationSeconds() {
    const durationElem = document.querySelector('.ytp-time-duration');
    if (!durationElem) return 0;

    const timeParts = durationElem.textContent.split(':').map(Number);

    // Supports both mm:ss and hh:mm:ss formats
    if (timeParts.length === 3) {
        return timeParts[0]*3600 + timeParts[1]*60 + timeParts[2];
    } else {
        return timeParts[0]*60 + timeParts[1];
    }
}

// Determines current playback resolution based on video height.
// This reflects actual streamed quality rather than selected quality label.
function getCurrentResolution() {
    const videoElement = document.querySelector('video');
    if (!videoElement) return "1080p";
    
    const height = videoElement.videoHeight;
    
    if (height <= 144) return "144p";
    if (height <= 240) return "240p";
    if (height <= 360) return "360p";
    if (height <= 480) return "480p";
    if (height <= 720) return "720p";
    if (height <= 1080) return "1080p";
    if (height <= 1440) return "1440p";
    if (height <= 2160) return "2160p";
    
    return "1080p";
}

// Estimates total video size in GB.
// Formula:
// Mbps × seconds = megabits
// ÷ 8 → megabytes
// ÷ 1024 → gigabytes
function estimateVideoSize(durationSeconds, resolution) {
    const bitrate = BITRATE_MAP[resolution] || BITRATE_MAP["1080p"];
    return (bitrate * durationSeconds) / (8 * 1024);
}

// Estimates data consumption per minute for dynamic impact comparison.
function estimateSizePerMinute(resolution) {
    const bitrate = BITRATE_MAP[resolution] || BITRATE_MAP["1080p"];
    return (bitrate * 60) / (8 * 1024);
}

// Assigns a visual color based on total CO2 impact.
// Used only for intuitive feedback (low = green, high = red).
function getColorByCO2(co2) {
    if (co2 < 10) return "#76FF03";
    if (co2 < 30) return "#FFC107";
    return "#FF3D00";
}

// Main function: calculates emissions and updates the UI panel.
function updateCO2Display() {

    const duration = getDurationSeconds();
    if (duration === 0) return;

    const resolution = getCurrentResolution();
    
    // Prevent recalculation if resolution has not changed.
    if (resolution === lastKnownResolution) return;
    lastKnownResolution = resolution;
    
    // Estimate total streamed data
    const sizeGB = estimateVideoSize(duration, resolution);

    // Convert data consumption to CO2 emissions
    const co2Total = (sizeGB * CO2_PER_GB).toFixed(2);

    // Calculate theoretical minimum and maximum emissions
    // Used to scale bottle fill level proportionally.
    const co2Min = estimateVideoSize(duration, getMinResolution()) * CO2_PER_GB;
    const co2Max = estimateVideoSize(duration, getMaxResolution()) * CO2_PER_GB;
    const co2Actual = sizeGB * CO2_PER_GB;

    const MAX_CO2 = 500;
    const SEGMENTS = 5;
    const SEGMENT_SIZE = MAX_CO2 / SEGMENTS; // 100g cada nivel

    // limited to max 500
    const cappedCO2 = Math.min(co2Actual, MAX_CO2);

    // in which segment is it
    const activeSegments = Math.ceil(cappedCO2 / SEGMENT_SIZE);

    // each segment is a 20%
    const waterPercent = (activeSegments / SEGMENTS) * 100;

    // Water consumption calculation (Data center + Network transmission)

    const liters = (
        sizeGB * (
            (WATER_DC_KWH_PER_GB * WUE_DC) +
            (WATER_NETWORK_KWH_PER_GB * WUE_NETWORK)
        )
    ).toFixed(2);
    
    // Calculate emissions per minute for comparison
    const sizePerMinuteGB = estimateSizePerMinute(resolution);
    const co2PerMinute = (sizePerMinuteGB * CO2_PER_GB).toFixed(2);

    // Create floating container if it does not exist
    let container = document.getElementById("co2-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "co2-container";
        container.style.position = "fixed";
        container.style.top = "20px";
        container.style.right = "20px";
        container.style.zIndex = "9999";
        container.style.fontFamily = "Arial, sans-serif";
        document.body.appendChild(container);
    }
    
    const formattedDuration = `${Math.floor(duration/60)}:${(duration%60).toString().padStart(2, '0')}`;
    const totalColor = getColorByCO2(parseFloat(co2Total));

    // Inject UI with updated values
    container.innerHTML = `
    <div style="
        background: rgba(30,30,30,0.75);
        color: #fff;
        padding: 12px 15px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.15);
        min-width: 260px;
        backdrop-filter: blur(8px);
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:15px;">

            <div style="flex:1;">
                <div style="margin-bottom: 10px;">
                    <div style="font-size: 13px; color: #aaa; margin-bottom: 3px;">Total for video</div>
                    <div style="font-size: 20px; font-weight: bold; color: ${totalColor};">${co2Total} g</div>
                </div>
                <div style="padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom:8px;">
                    <div style="font-size: 13px; color: #aaa; margin-bottom: 3px;">Per minute</div>
                    <div style="font-size: 16px; font-weight: bold; color: #fff;">${co2PerMinute} g/min</div>
                </div>
                <div style="font-size: 12px; color: #aaa; display: flex; justify-content: space-between;">
                    <span>${resolution}</span>
                    <span>${formattedDuration}</span>
                </div>
            </div>

            <div style="
                width:40px;
                height:100px;
                border:2px solid #fff;
                border-radius:12px;
                position:relative;
                overflow:hidden;
                background: linear-gradient(to top, #e6f7ff, #ffffff);
                display:flex;
                align-items:flex-end;
                justify-content:center;">
                <div style="
                    position:absolute;
                    bottom:0;
                    width:100%;
                    height:${waterPercent}%;
                    background: linear-gradient(to top, #00bfff, #66d9ff);
                    transition: height 0.6s ease;"></div>

                 ${[1,2,3,4].map(i => `<div style="
                        position:absolute;
                        bottom:${i * 20}%;
                        width:100%;
                        background:rgba(0,0,0,0.2);
                        pointer-events:none;"></div>`).join("")}

                <div style="
                    position:absolute;
                    top:0; left:0; width:100%; height:100%;
                    display:flex; align-items:center; justify-content:center;
                    font-size:10px; color:#000; font-weight:bold;
                    pointer-events:none;">${liters}L </div>
            </div>

        </div>
    </div>
    `;
}

// Detects resolution changes by monitoring video height.
function setupVideoObserver() {
    const videoElement = document.querySelector('video');
    if (!videoElement) return;

    let lastHeight = videoElement.videoHeight;
    
    const checkVideoChange = () => {
        if (videoElement.videoHeight !== lastHeight) {
            lastHeight = videoElement.videoHeight;
            updateCO2Display();
        }
    };

    setInterval(checkVideoChange, 1000);
}

// Detects when YouTube dynamically loads a new video.
function setupPageObserver() {
    const observer = new MutationObserver(() => {
        if (document.querySelector('video')) {
            const newVideoId = new URLSearchParams(window.location.search).get('v');
            if (newVideoId !== currentVideoId) {
                currentVideoId = newVideoId;
                lastKnownResolution = null;
                setTimeout(updateCO2Display, 1000);
                setTimeout(setupVideoObserver, 1500);
            }
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Initializes observers and periodic updates.
function init() {

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                updateCO2Display();
                setupPageObserver();
                setupVideoObserver();
            }, 2000);
        });
    } else {
        setTimeout(() => {
            updateCO2Display();
            setupPageObserver();
            setupVideoObserver();
        }, 2000);
    }

    // Periodic refresh to ensure UI remains updated.
    setInterval(updateCO2Display, 3000);
}

// Start execution
init();