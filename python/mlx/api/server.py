# Copyright © 2025 UMLX Contributors

"""
UMLX FastAPI Server

Provides REST API access to UMLX array operations and ML functionality.
Runs on port 1023 by default.
"""

import sys
from typing import List, Optional, Union

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("FastAPI dependencies not installed. Install with: pip install mlx[api]")
    sys.exit(1)

# Try to import mlx.core, but allow the module to load without it for testing
try:
    import mlx.core as mx
    MLX_AVAILABLE = True
except ImportError:
    MLX_AVAILABLE = False
    mx = None

# Import version
try:
    from mlx._version import __version__ as UMLX_VERSION
except ImportError:
    UMLX_VERSION = "0.30.3"  # Fallback version


# Pydantic models for request/response validation
class ArrayCreate(BaseModel):
    """Model for creating an array"""
    data: List[Union[int, float, List]]
    dtype: Optional[str] = Field(default=None, description="Data type (float32, int32, etc.)")


class ArrayInfo(BaseModel):
    """Model for array information response"""
    shape: List[int]
    dtype: str
    size: int
    ndim: int


class ArrayOperation(BaseModel):
    """Model for binary array operations"""
    operation: str = Field(..., description="Operation name (add, subtract, multiply, divide)")
    array1: List[Union[int, float, List]]
    array2: List[Union[int, float, List]]


class DeviceInfo(BaseModel):
    """Model for device information"""
    device_type: str
    default_device: str


class DeviceSet(BaseModel):
    """Model for setting device"""
    device: str = Field(..., description="Device to set (cpu or gpu)")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    devices: List[str]


# Initialize FastAPI app
app = FastAPI(
    title="UMLX API",
    description="Universal MLX REST API for cross-platform machine learning operations",
    version=UMLX_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "UMLX API Server",
        "version": UMLX_VERSION,
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    try:
        # Get available devices
        devices = []
        if MLX_AVAILABLE:
            try:
                devices.append(f"mlx: {mx.default_device()}")
            except Exception:
                devices.append("mlx: available")
        else:
            devices.append("mlx: not installed")
        
        return HealthResponse(
            status="healthy",
            version=UMLX_VERSION,
            devices=devices,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/array/create", response_model=dict)
async def create_array(array_data: ArrayCreate):
    """Create an MLX array"""
    if not MLX_AVAILABLE:
        raise HTTPException(status_code=503, detail="MLX core not available. Install mlx package.")
    
    try:
        if array_data.dtype:
            arr = mx.array(array_data.data, dtype=getattr(mx, array_data.dtype))
        else:
            arr = mx.array(array_data.data)
        
        return {
            "shape": list(arr.shape),
            "dtype": str(arr.dtype),
            "size": int(arr.size),
            "ndim": int(arr.ndim),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Array creation failed: {str(e)}")


@app.get("/array/info", response_model=ArrayInfo)
async def array_info(shape: str, dtype: str = "float32"):
    """Get information about an array with given shape and dtype"""
    if not MLX_AVAILABLE:
        raise HTTPException(status_code=503, detail="MLX core not available. Install mlx package.")
    
    try:
        shape_tuple = tuple(map(int, shape.split(",")))
        arr = mx.zeros(shape_tuple, dtype=getattr(mx, dtype))
        
        return ArrayInfo(
            shape=list(arr.shape),
            dtype=str(arr.dtype),
            size=int(arr.size),
            ndim=int(arr.ndim),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Array info failed: {str(e)}")


@app.post("/array/operation", response_model=dict)
async def array_operation(op: ArrayOperation):
    """Perform a binary operation on two arrays"""
    if not MLX_AVAILABLE:
        raise HTTPException(status_code=503, detail="MLX core not available. Install mlx package.")
    
    try:
        arr1 = mx.array(op.array1)
        arr2 = mx.array(op.array2)
        
        operations = {
            "add": lambda a, b: a + b,
            "subtract": lambda a, b: a - b,
            "multiply": lambda a, b: a * b,
            "divide": lambda a, b: a / b,
            "matmul": lambda a, b: a @ b,
        }
        
        if op.operation not in operations:
            raise ValueError(f"Unknown operation: {op.operation}")
        
        result = operations[op.operation](arr1, arr2)
        mx.eval(result)
        
        return {
            "result": result.tolist(),
            "shape": list(result.shape),
            "dtype": str(result.dtype),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Operation failed: {str(e)}")


@app.get("/devices", response_model=DeviceInfo)
async def get_devices():
    """Get available device information"""
    if not MLX_AVAILABLE:
        raise HTTPException(status_code=503, detail="MLX core not available. Install mlx package.")
    
    try:
        default = str(mx.default_device())
        device_type = default.split("(")[0] if "(" in default else default
        
        return DeviceInfo(
            device_type=device_type,
            default_device=default,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Device query failed: {str(e)}")


@app.post("/device/set", response_model=dict)
async def set_device(device_set: DeviceSet):
    """Set the default device"""
    if not MLX_AVAILABLE:
        raise HTTPException(status_code=503, detail="MLX core not available. Install mlx package.")
    
    try:
        if device_set.device.lower() == "cpu":
            mx.set_default_device(mx.cpu)
        elif device_set.device.lower() == "gpu":
            mx.set_default_device(mx.gpu)
        else:
            raise ValueError(f"Unknown device: {device_set.device}")
        
        return {
            "status": "success",
            "device": str(mx.default_device()),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Device set failed: {str(e)}")


def start_server(host: str = "0.0.0.0", port: int = 1023, reload: bool = False):
    """
    Start the UMLX API server
    
    Args:
        host: Host to bind to (default: 0.0.0.0)
        port: Port to bind to (default: 1023)
        reload: Enable auto-reload for development
    """
    uvicorn.run(
        "mlx.api.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


def main():
    """CLI entry point for starting the server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="UMLX API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=1023, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    print(f"Starting UMLX API server on {args.host}:{args.port}")
    print(f"Documentation available at http://{args.host}:{args.port}/docs")
    
    start_server(host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
