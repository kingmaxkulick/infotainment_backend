"""
Core constants including CAN IDs and message definitions
"""

# Vehicle Data IDs 
CAN_IDS = {
    "charge_percentage": 0x101,
    "charging_rate": 0x102,
    "estimated_full_charge_time": 0x103,
    "battery_temp": 0x104,
    "motor_temp": 0x201,
    "inverter_temp": 0x202,
    "tire_temp": 0x301,
    "tire_pressure": 0x302,
    "power_output": 0x401,
    "torque_distribution": 0x402,
    "suspension_metrics": 0x403,
    "g_forces": 0x404,
    "brake_temp": 0x405,
    "vehicle_state": 0x600,
    "fault_status": 0x601
}

# Vehicle States (0x600)
VEHICLE_STATES = {
    0x01: "PARK",
    0x02: "DRIVE",
    0x03: "REVERSE",
    0x04: "NEUTRAL",
    0x05: "CHARGE"
}

VEHICLE_SUBSTATES = {
    0x01: "INITIALIZING",
    0x02: "READY",
    0x03: "ACTIVE",
    0x04: "COMPLETE"
}

STATUS_FLAGS = {
    0x01: "DOOR_OPEN",
    0x02: "CHARGING_CONNECTED",
    0x04: "MOTOR_READY",
    0x08: "BATTERY_OK",
    0x10: "SYSTEMS_CHECK_PASS"
}

# Fault Information (0x601)
FAULT_SOURCES = {
    0x01: "BATTERY",
    0x02: "MOTOR",
    0x03: "CHARGING",
    0x04: "TIRE",
    0x05: "POWER"
}

FAULT_TYPES = {
    0x01: "TEMP_HIGH",
    0x02: "TEMP_LOW",
    0x03: "PRESSURE_HIGH",
    0x04: "PRESSURE_LOW",
    0x05: "CURRENT_HIGH",
    0x06: "VOLTAGE_HIGH",
    0x07: "VOLTAGE_LOW",
    0x08: "COMM_ERROR"
}