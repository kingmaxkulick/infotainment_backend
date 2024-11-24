"""
Vehicle data models and state tracking
"""

from typing import List, Optional
from pydantic import BaseModel
from ..core.constants import (
    VEHICLE_STATES,
    VEHICLE_SUBSTATES,
    STATUS_FLAGS,
    FAULT_SOURCES,
    FAULT_TYPES
)

class VehicleState(BaseModel):
    primary_state: str = "PARK"
    sub_state: str = "READY"
    status_flags: List[str] = []
    fault_present: bool = False
    message_counter: int = 0

class FaultStatus(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    severity: int = 0
    timestamp: int = 0
    counter: int = 0
    active: bool = False

class VehicleData(BaseModel):
    # Basic metrics
    charge_percent: int = 0
    charging_rate: int = 0
    full_charge_time: int = 0
    
    # Temperatures
    battery_temp: int = 0
    motor_temp: int = 0
    inverter_temp: int = 0
    brake_temp: int = 0
    
    # Tire data
    tire_temp: List[int] = [0, 0, 0, 0]
    tire_pressure: List[int] = [0, 0, 0, 0]
    
    # Performance metrics
    power_output: int = 0
    torque_distribution: List[int] = [0, 0, 0, 0]
    suspension_metrics: List[int] = [0, 0, 0, 0]
    g_forces: List[int] = [0, 0, 0]
    
    # State and fault tracking
    vehicle_state: VehicleState = VehicleState()
    fault_status: FaultStatus = FaultStatus()

# Global instance for real-time data
vehicle_data = VehicleData()

def update_vehicle_state(data: bytes) -> None:
    """Update vehicle state from CAN message (0x600)"""
    state = VEHICLE_STATES.get(data[0], "UNKNOWN")
    substate = VEHICLE_SUBSTATES.get(data[1], "UNKNOWN")
    
    # Decode status flags
    flags = []
    for flag_bit, flag_name in STATUS_FLAGS.items():
        if data[2] & flag_bit:
            flags.append(flag_name)
    
    # Update state
    vehicle_data.vehicle_state.primary_state = state
    vehicle_data.vehicle_state.sub_state = substate
    vehicle_data.vehicle_state.status_flags = flags
    vehicle_data.vehicle_state.fault_present = bool(data[3])
    vehicle_data.vehicle_state.message_counter = (data[4] << 8) | data[5]

def update_fault_status(data: bytes) -> None:
    """Update fault status from CAN message (0x601)"""
    vehicle_data.fault_status.source = FAULT_SOURCES.get(data[0])
    vehicle_data.fault_status.type = FAULT_TYPES.get(data[1])
    vehicle_data.fault_status.severity = data[2]
    vehicle_data.fault_status.timestamp = (data[3] << 24) | (data[4] << 16) | \
                                        (data[5] << 8) | data[6]
    vehicle_data.fault_status.counter = data[7]
    vehicle_data.fault_status.active = bool(data[2])  # Active if severity > 0

def get_vehicle_data() -> dict:
    """Get current vehicle data as dictionary"""
    return vehicle_data.model_dump()

def update_metric(metric: str, value: int | List[int]) -> None:
    """Update a single vehicle metric"""
    if hasattr(vehicle_data, metric):
        setattr(vehicle_data, metric, value)