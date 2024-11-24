import asyncio
import can
from app.models import vehicle_data, CAN_IDS

# CAN message handler
async def read_can_data():
    bus = can.interface.Bus(channel="can0", bustype="socketcan")

    while True:
        message = bus.recv()  # Wait for a message from the CAN bus

        if message is not None:
            # Update vehicle_data based on CAN IDs
            if message.arbitration_id == CAN_IDS["charge_percentage"]:
                vehicle_data["charge_percent"] = message.data[0]

            elif message.arbitration_id == CAN_IDS["charging_rate"]:
                vehicle_data["charging_rate"] = message.data[0]

            elif message.arbitration_id == CAN_IDS["estimated_full_charge_time"]:
                vehicle_data["full_charge_time"] = message.data[0]

            elif message.arbitration_id == CAN_IDS["battery_temp"]:
                vehicle_data["battery_temp"] = message.data[0]

            elif message.arbitration_id == CAN_IDS["motor_temp"]:
                vehicle_data["motor_temp"] = message.data[0]

            elif message.arbitration_id == CAN_IDS["inverter_temp"]:
                vehicle_data["inverter_temp"] = message.data[0]

            elif message.arbitration_id == CAN_IDS["tire_temp"]:
                vehicle_data["tire_temp"] = list(message.data[:4])

            elif message.arbitration_id == CAN_IDS["tire_pressure"]:
                vehicle_data["tire_pressure"] = list(message.data[:4])

            elif message.arbitration_id == CAN_IDS["power_output"]:
                vehicle_data["power_output"] = message.data[0]

            elif message.arbitration_id == CAN_IDS["torque_distribution"]:
                vehicle_data["torque_distribution"] = list(message.data[:4])

            elif message.arbitration_id == CAN_IDS["suspension_metrics"]:
                vehicle_data["suspension_metrics"] = list(message.data[:4])

            elif message.arbitration_id == CAN_IDS["g_forces"]:
                vehicle_data["g_forces"] = list(message.data[:3])

            elif message.arbitration_id == CAN_IDS["brake_temp"]:
                vehicle_data["brake_temp"] = message.data[0]

        await asyncio.sleep(0.1)  # Adjust interval as needed
