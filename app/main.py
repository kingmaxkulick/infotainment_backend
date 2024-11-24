"""
Main FastAPI application
"""
import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import router
from .services.can_service import CANService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Vehicle HMI API",
    description="API for vehicle data and status information",
    version="2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Create CAN service instance
can_service = CANService()

@app.on_event("startup")
async def startup_event():
    """Start CAN service when API starts"""
    try:
        # Start CAN service in background task
        asyncio.create_task(can_service.run())
        logger.info("CAN service started successfully")
    except Exception as e:
        logger.error(f"Failed to start CAN service: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Stop CAN service when API stops"""
    await can_service.stop()
    logger.info("CAN service stopped")