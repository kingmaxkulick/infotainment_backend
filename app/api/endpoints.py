"""
FastAPI endpoints for vehicle data access
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..models.vehicle_data import get_vehicle_data, vehicle_data
from ..models.vehicle_data import VehicleState, FaultStatus

router = APIRouter()

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Vehicle HMI API",
        "version": "2.0",
        "status": "running"
    }

@router.get("/vehicle_data")
async def get_all_vehicle_data() -> Dict[str, Any]:
    """Get all vehicle data including state and faults"""
    return get_vehicle_data()

@router.get("/vehicle_state")
async def get_vehicle_state() -> VehicleState:
    """Get current vehicle state information"""
    return vehicle_data.vehicle_state

@router.get("/fault_status")
async def get_fault_status() -> FaultStatus:
    """Get current fault status"""
    return vehicle_data.fault_status

@router.get("/metrics/powertrain")
async def get_powertrain_metrics():
    """Get powertrain-related metrics"""
    return {
        "charge_percent": vehicle_data.charge_percent,
        "battery_temp": vehicle_data.battery_temp,
        "motor_temp": vehicle_data.motor_temp,
        "power_output": vehicle_data.power_output
    }

@router.get("/metrics/tires")
async def get_tire_metrics():
    """Get tire-related metrics"""
    return {
        "tire_temp": vehicle_data.tire_temp,
        "tire_pressure": vehicle_data.tire_pressure
    }

@router.get("/health")
async def get_health_status():
    """Get API and vehicle health status"""
    # Check if we're receiving state messages
    state_healthy = vehicle_data.vehicle_state.message_counter > 0
    
    # Check for active faults
    fault_active = vehicle_data.fault_status.active
    
    return {
        "api_status": "healthy",
        "receiving_messages": state_healthy,
        "fault_active": fault_active,
        "last_state_counter": vehicle_data.vehicle_state.message_counter
    }