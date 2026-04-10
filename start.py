#!/usr/bin/env python3
"""
Quick Start Script for IV Monitoring System
Checks dependencies, initializes database, and starts the backend
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Verify Python 3.9+ is installed"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'sqlalchemy': 'sqlalchemy',
        'pydantic': 'pydantic',
    }

    missing = []
    for package_name, import_name in required_packages.items():
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            missing.append(package_name)
        else:
            print(f"✓ {package_name} installed")

    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nInstalling dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed")

    return len(missing) == 0


def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("\n📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write("""# IV Monitoring System Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./iv_monitoring.db
""")
        print("✓ .env file created (customize as needed)")
    else:
        print("✓ .env file exists")


def init_database():
    """Initialize database"""
    print("\n🗄️  Initializing database...")
    try:
        from models import init_db
        import config
        engine = init_db(config.DATABASE_URL)
        print("✓ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization: {e}")


def start_backend():
    """Start the FastAPI backend"""
    print("\n" + "="*60)
    print("  IV MONITORING SYSTEM - BACKEND STARTING")
    print("="*60)
    print("\n✓ Backend server running at http://localhost:8000")
    print("✓ API Documentation: http://localhost:8000/docs")
    print("✓ Alternative Docs: http://localhost:8000/redoc")
    print("\n📝 Run test_api.py in another terminal to test endpoints")
    print("📝 Press Ctrl+C to stop the server\n")

    try:
        import app
        import uvicorn
        uvicorn.run(
            app.app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False
        )
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)


def main():
    """Main startup sequence"""
    print("\n" + "="*60)
    print("  IV MONITORING SYSTEM - QUICK START")
    print("="*60 + "\n")

    print("📋 Checking requirements...\n")

    # Check Python version
    check_python_version()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Create .env file
    create_env_file()

    # Initialize database
    init_database()

    # Start backend
    start_backend()


if __name__ == "__main__":
    main()
