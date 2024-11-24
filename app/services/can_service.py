"""
CAN message handling service
"""
import asyncio
import can
import logging
from typing import Optional
from ..core.constants import CAN_IDS
from ..models.vehicle_data import (
    vehicle_data,
    update_vehicle_state,
    update_fault_status,
    update_metric
)

logger = logging.getLogger(__name__)

class CANService:
    def __init__(self):
        self.bus: Optional[can.Bus] = None
        self._running = False
        self._last_state_counter = 0
        self._last_message_times = {}  # Track last message time for each ID

    async def start(self):
        """Start the CAN service"""
        try:
            self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
            self._running = True
            logger.info("CAN service started successfully")
        except Exception as e:
            logger.error(f"Failed to start CAN service: {e}")
            raise

    async def stop(self):
        """Stop the CAN service"""
        self._running = False
        if self.bus:
            self.bus.shutdown()
        logger.info("CAN service stopped")

    def decode_message(self, msg: can.Message) -> None:
        """Decode and process a CAN message"""
        try:
            # Track message receipt time
            self._last_message_times[msg.arbitration_id] = asyncio.get_event_loop().time()

            # Handle vehicle state message (0x600)
            if msg.arbitration_id == CAN_IDS["vehicle_state"]:
                update_vehicle_state(msg.data)
                # Check for missed messages
                new_counter = (msg.data[4] << 8) | msg.data[5]
                if self._last_state_counter > 0:
                    expected = (self._last_state_counter + 1) % 65536
                    if new_counter != expected:
                        logger.warning(f"Missed state message(s). Expected {expected}, got {new_counter}")
                self._last_state_counter = new_counter

            # Handle fault status message (0x601)
            elif msg.arbitration_id == CAN_IDS["fault_status"]:
                update_fault_status(msg.data)

            # Handle metric messages
            elif msg.arbitration_id == CAN_IDS["charge_percentage"]:
                update_metric("charge_percent", msg.data[0])
            
            elif msg.arbitration_id == CAN_IDS["battery_temp"]:
                update_metric("battery_temp", msg.data[0])
            
            elif msg.arbitration_id == CAN_IDS["motor_temp"]:
                update_metric("motor_temp", msg.data[0])
                
            elif msg.arbitration_id == CAN_IDS["tire_temp"]:
                update_metric("tire_temp", list(msg.data[:4]))
                
            elif msg.arbitration_id == CAN_IDS["tire_pressure"]:
                update_metric("tire_pressure", list(msg.data[:4]))
                
            elif msg.arbitration_id == CAN_IDS["power_output"]:
                update_metric("power_output", msg.data[0])

        except Exception as e:
            logger.error(f"Error processing CAN message {hex(msg.arbitration_id)}: {e}")

    async def monitor_timeouts(self):
        """Monitor for message timeouts"""
        while self._running:
            current_time = asyncio.get_event_loop().time()
            
            # Check high priority messages (should arrive every 100ms)
            high_priority = [
                ("vehicle_state", 0.2),  # 200ms timeout
                ("fault_status", 0.2),
                ("power_output", 0.2)
            ]
            
            # Check medium priority messages (should arrive every 200ms)
            medium_priority = [
                ("motor_temp", 0.4),  # 400ms timeout
                ("battery_temp", 0.4)
            ]
            
            # Check all timeouts
            for msg_name, timeout in high_priority + medium_priority:
                msg_id = CAN_IDS[msg_name]
                last_time = self._last_message_times.get(msg_id)
                if last_time and (current_time - last_time) > timeout:
                    logger.warning(f"Timeout: No {msg_name} message for {timeout}s")
            
            await asyncio.sleep(0.1)

    async def run(self):
        """Main service loop"""
        if not self.bus:
            await self.start()

        # Start timeout monitor
        timeout_monitor = asyncio.create_task(self.monitor_timeouts())
        
        try:
            while self._running:
                try:
                    # Non-blocking message receive
                    msg = self.bus.recv(timeout=0.1)
                    if msg:
                        self.decode_message(msg)
                    await asyncio.sleep(0.001)  # Yield to other tasks
                except Exception as e:
                    logger.error(f"Error in CAN service loop: {e}")
                    await asyncio.sleep(1)  # Wait before retrying
                    
        finally:
            timeout_monitor.cancel()
            await self.stop()