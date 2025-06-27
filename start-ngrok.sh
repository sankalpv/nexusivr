#!/bin/bash

# Check if ngrok is installed globally or in the local bin directory
if command -v ngrok &> /dev/null; then
    NGROK_CMD="ngrok"
elif [ -f "bin/ngrok" ]; then
    NGROK_CMD="./bin/ngrok"
else
    echo "Error: ngrok is not installed or not found"
    echo "Please install ngrok using one of the following methods:"
    echo "  - Run ./download-ngrok.sh to download ngrok to the bin directory"
    echo "  - brew install ngrok"
    echo "  - npm install -g ngrok"
    echo "  - Download from https://ngrok.com/download"
    exit 1
fi

# Default port for FastAPI
PORT=8000

# Check if a port was provided as an argument
if [ $# -eq 1 ]; then
    PORT=$1
fi

echo "Starting ngrok tunnel to localhost:$PORT..."
echo "This will expose your FastAPI backend server to the internet."
echo "Use the HTTPS URL provided by ngrok in your Twilio webhook configuration."
echo "Press Ctrl+C to stop the tunnel."
echo ""

# Start ngrok
$NGROK_CMD http $PORT
