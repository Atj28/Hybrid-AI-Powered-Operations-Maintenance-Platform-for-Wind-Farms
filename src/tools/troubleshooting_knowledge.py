# troubleshooting_knowledge.py

TROUBLESHOOTING_KB = {
    "GEARBOX_OVERHEAT": {
        "description": "Gearbox oil temperature is above safe limit.",
        "possible_causes": [
            "Insufficient oil level",
            "Blocked oil cooler or poor cooling",
            "High ambient temperature combined with high load",
            "Degradation of oil (old or contaminated)"
        ],
        "checks": [
            "Check gearbox oil level and look for leaks.",
            "Inspect oil cooler for blockages or fan failure.",
            "Verify temperature sensors are reading correctly.",
            "Review recent operating conditions (high wind / high load)."
        ],
        "recommended_actions": [
            "Reduce turbine loading if possible (temporary derating).",
            "Schedule inspection of gearbox and cooling system.",
            "Take oil sample for analysis if overheating is frequent.",
            "Log the event and monitor trend for repeated occurrences."
        ],
        "severity": "HIGH"
    },
    "HIGH_VIBRATION": {
        "description": "Measured vibration exceeds normal operating limits.",
        "possible_causes": [
            "Rotor blade imbalance or contamination (ice/dirt).",
            "Bearing wear or misalignment.",
            "Loose foundation or structural looseness.",
            "Gear mesh issues or damaged components."
        ],
        "checks": [
            "Inspect blades for dirt, ice, or physical damage.",
            "Check main shaft and gearbox bearings for abnormal noise.",
            "Verify vibration sensor mounting and wiring.",
            "Review vibration trend and compare with historical baseline."
        ],
        "recommended_actions": [
            "If vibration is very high, stop turbine and inspect before restart.",
            "Plan a detailed vibration analysis (condition monitoring).",
            "Tighten mechanical connections if looseness is detected.",
            "Involve OEM/service engineer if this repeats."
        ],
        "severity": "HIGH"
    },
    "PITCH_STUCK": {
        "description": "Pitch system not responding; blades may be stuck at one angle.",
        "possible_causes": [
            "Hydraulic/electric pitch actuator failure.",
            "Pitch communication/control fault.",
            "Mechanical blockage in hub or pitch bearing.",
        ],
        "checks": [
            "Check pitch system alarms and error codes.",
            "Verify hydraulic pressure or electrical supply to pitch system.",
            "Inspect hub area (if safe and allowed by procedures)."
        ],
        "recommended_actions": [
            "Keep turbine stopped until pitch system is inspected.",
            "Escalate to OEM/support if multiple pitch faults occur.",
            "Do not attempt manual override without following safety SOP."
        ],
        "severity": "CRITICAL"
    },
    "YAW_MISALIGNMENT": {
        "description": "Turbine nacelle is misaligned with wind direction, causing power loss.",
        "possible_causes": [
            "Yaw sensor offset or failure.",
            "Yaw drive or brake malfunction.",
            "Control parameter issue (yaw deadband too large)."
        ],
        "checks": [
            "Compare nacelle direction with met mast or LIDAR data if available.",
            "Check yaw system alarms and status.",
            "Inspect yaw drive, brakes, and cabling."
        ],
        "recommended_actions": [
            "Recalibrate yaw position sensor if needed.",
            "Schedule yaw system inspection.",
            "Reduce yaw deadband if recommended by OEM."
        ],
        "severity": "MEDIUM"
    },
    "GRID_EVENT": {
        "description": "Grid-related event affecting turbine output (curtailment, low voltage, frequency issues).",
        "possible_causes": [
            "Grid operator curtailment order.",
            "Voltage dips or frequency deviations.",
            "Substation or line constraints."
        ],
        "checks": [
            "Check grid operator instructions and curtailment logs.",
            "Review substation SCADA for voltage/frequency events.",
            "Verify reactive power/voltage control settings."
        ],
        "recommended_actions": [
            "Quantify energy loss due to curtailment.",
            "Coordinate with grid operator for future planning.",
            "Ensure protection and control settings meet grid code."
        ],
        "severity": "LOW to MEDIUM"
    },
    "NO_FAULT": {
        "description": "No specific fault detected based on current rules.",
        "possible_causes": ["Normal operation or minor deviation within tolerance."],
        "checks": ["Monitor trends over time to catch early issues if they grow."],
        "recommended_actions": ["No immediate action required; continue monitoring."],
        "severity": "NONE"
    }
}
