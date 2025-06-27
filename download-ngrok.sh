#!/bin/bash

# Script to download and set up ngrok directly

# Create bin directory if it doesn't exist
mkdir -p bin

# Determine system architecture
ARCH=$(uname -m)
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

# Set download URL based on architecture
if [ "$OS" == "darwin" ]; then
    if [ "$ARCH" == "arm64" ]; then
        URL="https://bin.ngrok.com/v3/ngrok-v3-stable-darwin-arm64.zip"
    else
        URL="https://bin.ngrok.com/v3/ngrok-v3-stable-darwin-amd64.zip"
    fi
elif [ "$OS" == "linux" ]; then
    if [ "$ARCH" == "arm64" ] || [ "$ARCH" == "aarch64" ]; then
        URL="https://bin.ngrok.com/v3/ngrok-v3-stable-linux-arm64.zip"
    else
        URL="https://bin.ngrok.com/v3/ngrok-v3-stable-linux-amd64.zip"
    fi
else
    echo "Unsupported operating system: $OS"
    exit 1
fi

echo "Downloading ngrok for $OS-$ARCH..."
echo "URL: $URL"

# Download ngrok
curl -o bin/ngrok.zip "$URL"

# Check if download was successful
if [ $? -ne 0 ]; then
    echo "Failed to download ngrok. Please check your internet connection and try again."
    exit 1
fi

# Unzip the downloaded file
echo "Extracting ngrok..."
unzip -o bin/ngrok.zip -d bin

# Make ngrok executable
chmod +x bin/ngrok

# Clean up
rm bin/ngrok.zip

echo "ngrok has been downloaded to bin/ngrok"
echo "You can run it using: ./bin/ngrok http 8000"
echo ""
echo "For convenience, you can also use the start-ngrok.sh script:"
echo "./start-ngrok.sh"
