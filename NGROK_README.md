# Ngrok Setup for Nexus IVR

This directory contains scripts and documentation for setting up ngrok with the Nexus IVR project.

## Files

- `start-ngrok.sh`: Script to start ngrok and expose your FastAPI backend server to the internet.
- `download-ngrok.sh`: Script to download and set up ngrok directly in the project's `bin` directory.
- `NGROK_SETUP.md`: Detailed documentation on installing and using ngrok with this project.

## Quick Start

1. **Install ngrok** using one of the methods described in `NGROK_SETUP.md`.

2. **Start your FastAPI backend server**:
   ```sh
   cd backend
   # Set up virtual environment if needed
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install fastapi uvicorn twilio
   
   # Start the server
   uvicorn main:app --reload
   ```

3. **Start ngrok** in a new terminal:
   ```sh
   ./start-ngrok.sh
   ```

4. **Configure Twilio** with the ngrok URL as described in `backend/TWILIO_SETUP.md`.

## Troubleshooting

If you encounter issues with ngrok installation or usage, please refer to the detailed troubleshooting section in `NGROK_SETUP.md`.

## Network Issues

If you're experiencing network connectivity issues with downloading ngrok, you can:

1. Try using the `download-ngrok.sh` script which attempts to download directly from the ngrok website.
2. Download ngrok manually from [ngrok's download page](https://ngrok.com/download) and place it in the `bin` directory.
3. Check your network connectivity and DNS resolution.
