#!/usr/bin/env python
# Copyright © 2025 UMLX Contributors

"""
Simple validation test for UMLX API server
Tests basic endpoints without requiring mlx.core
"""

import sys
import time
import json
from pathlib import Path

# Add python directory to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

def test_api_imports():
    """Test that API modules can be imported"""
    print("Testing API imports...")
    try:
        from mlx.api import server
        print("✓ Successfully imported mlx.api.server")
        
        # Check FastAPI app exists
        assert hasattr(server, 'app'), "FastAPI app not found"
        print("✓ FastAPI app exists")
        
        # Check main endpoints exist
        routes = [route.path for route in server.app.routes]
        expected_routes = [
            "/",
            "/health", 
            "/array/create",
            "/array/info",
            "/array/operation",
            "/devices",
            "/device/set"
        ]
        
        for route in expected_routes:
            if route in routes:
                print(f"✓ Route {route} exists")
            else:
                print(f"✗ Route {route} missing")
                return False
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        print("  Make sure FastAPI is installed: pip install fastapi uvicorn pydantic")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def test_api_structure():
    """Test API structure and models"""
    print("\nTesting API structure...")
    try:
        from mlx.api import server
        from mlx._version import __version__ as UMLX_VERSION
        
        # Check Pydantic models exist
        models = [
            'ArrayCreate',
            'ArrayInfo', 
            'ArrayOperation',
            'DeviceInfo',
            'DeviceSet',
            'HealthResponse'
        ]
        
        for model in models:
            if hasattr(server, model):
                print(f"✓ Model {model} exists")
            else:
                print(f"✗ Model {model} missing")
                return False
        
        # Check app metadata
        assert server.app.title == "UMLX API", f"Wrong app title: {server.app.title}"
        print(f"✓ App title correct: {server.app.title}")
        
        assert server.app.version == UMLX_VERSION, f"Wrong version: {server.app.version} (expected {UMLX_VERSION})"
        print(f"✓ App version correct: {server.app.version}")
        
        return True
    except Exception as e:
        print(f"✗ Structure test failed: {e}")
        return False

def test_api_documentation():
    """Test that API documentation is configured"""
    print("\nTesting API documentation...")
    try:
        from mlx.api import server
        
        assert server.app.docs_url == "/docs", "Swagger docs URL incorrect"
        print(f"✓ Swagger docs at {server.app.docs_url}")
        
        assert server.app.redoc_url == "/redoc", "ReDoc URL incorrect"
        print(f"✓ ReDoc at {server.app.redoc_url}")
        
        return True
    except Exception as e:
        print(f"✗ Documentation test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("="*60)
    print("UMLX API Validation Tests")
    print("="*60)
    
    tests = [
        ("Import Test", test_api_imports),
        ("Structure Test", test_api_structure),
        ("Documentation Test", test_api_documentation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All validation tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
