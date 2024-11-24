# In-memory data store to keep CAN data
# eventually have more than one dict
vehicle_data = {
    "charge_percent": 0,
    "charging_rate": 0,
    "full_charge_time": 0,
    "battery_temp": 0,
    "motor_temp": 0,
    "inverter_temp": 0,
    "tire_temp": [0, 0, 0, 0],
    "tire_pressure": [0, 0, 0, 0],
    "power_output": 0,
    "torque_distribution": [0, 0, 0, 0],
    "suspension_metrics": [0, 0, 0, 0],
    "g_forces": [0, 0, 0],
    "brake_temp": 0,
}

# CAN IDs for different data types
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
}
