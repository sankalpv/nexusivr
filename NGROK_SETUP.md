# Ngrok Setup for Nexus IVR

This guide explains how to use ngrok to expose your local FastAPI backend server to the internet, allowing Twilio to communicate with your IVR system.

## What is ngrok?

Ngrok is a tool that creates secure tunnels to localhost, making your locally running web servers accessible from the internet. This is essential for services like Twilio that need to send webhooks to your application.

## Installation

There are several ways to install ngrok:

### Option 1: Using Homebrew (macOS)

```sh
brew install ngrok
```

### Option 2: Using npm

```sh
# Install globally
npm install -g ngrok

# Or as a dev dependency in your project
npm install --save-dev ngrok
```

### Option 3: Using the Provided Script

We've included a script to download ngrok directly:

```sh
# Make the script executable
chmod +x download-ngrok.sh

# Run the script to download ngrok
./download-ngrok.sh
```

This script will:
1. Detect your system architecture
2. Download the appropriate ngrok binary
3. Extract it to the `bin` directory
4. Make it executable

### Option 4: Direct Download

Download the appropriate binary for your system from [ngrok's download page](https://ngrok.com/download).

### Option 5: Using LocalTunnel (Alternative to ngrok)

You can use [LocalTunnel](https://github.com/localtunnel/localtunnel) as a free alternative to ngrok:

```sh
npm install -g localtunnel
lt --port 8000
```

This will give you a public URL like `https://happy-bags-add.loca.lt`.

## Using ngrok or LocalTunnel with Nexus IVR

1. **Start your FastAPI backend server**:

   ```sh
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt  # If you have a requirements.txt file
   pip install fastapi uvicorn twilio  # If you don't have a requirements.txt
   uvicorn main:app --reload
   ```

   This will start your FastAPI server on port 8000 (default).

2. **Start ngrok** (in a new terminal):

   ```sh
   # Using the provided script
   ./start-ngrok.sh
   
   # Or directly
   ngrok http 8000
   ```

   **Or start LocalTunnel:**

   ```sh
   lt --port 8000
   ```

3. **Note the HTTPS URL** provided by ngrok or LocalTunnel (e.g., `https://happy-bags-add.loca.lt`).

4. **Configure Twilio**:
   - In your Twilio Console, go to your phone number settings.
   - Set the Voice webhook (for incoming calls) to:
     ```
     https://happy-bags-add.loca.lt/ivr/answer
     ```
   - Use HTTP POST method.

## Important Notes

- The ngrok URL changes each time you restart ngrok unless you have a paid account.
- You'll need to update your Twilio webhook URL each time the ngrok URL changes.
- Keep both your FastAPI server and ngrok running while testing with Twilio.
- For production use, deploy your application to a proper hosting service instead of using ngrok.

## Troubleshooting

- If you get "ngrok not found", make sure it's installed and in your PATH.
- If you see connection errors, ensure your FastAPI server is running on the correct port.
- If Twilio can't reach your webhook, verify the ngrok URL is correct and your FastAPI server is handling the route properly.
