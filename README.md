# JBL Playlist (FSAPI) - Keep Alive

JBL Playlist when connected through cable is always goes to sleep when there is no audio playing or the volume is too low. This script keeps the JBL speaker alive by sending keep alive requests to the speaker's fsapi.

## Features

- Automatically checks if your PC is online (optional)
- Keeps the JBL speaker on when the PC is detected or always if no PC address is specified
- Optionally uses play state instead of power state to control the speaker
- Can turn off the speaker when the PC is off (optional)
- Can run as a background service
- Easy to configure and set up
- Uses FSAPI to control the speaker

## Prerequisites

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository or download the `main.py` and `setup.py` files.

2. Install the required Python library:

   ```
   pip3 install -r requirements.txt
   ```

## Docker Usage

You can also run this application using Docker and Docker Compose.

### Prerequisites

- Docker
- Docker Compose v2 (included with Docker Desktop or install separately)

### Quick Start

1. Create a `.env` file (optional) or set environment variables:

   ```bash
   # Required
   JBL_ADDRESS=192.168.1.200
   
   # Optional
   PC_ADDRESS=192.168.1.100
   JBL_PORT=80
   JBL_PIN=1234
   INTERVAL=60
   ```

2. Build and run with Docker Compose:

   ```bash
   docker compose up -d
   ```

3. View logs:

   ```bash
   docker compose logs -f
   ```

4. Stop the container:

   ```bash
   docker compose down
   ```

### Environment Variables

- `PC_ADDRESS`: IP address of the PC (optional). Leave empty to always keep the speaker on.
- `JBL_ADDRESS`: IP address of the JBL speaker (required, default: 192.168.1.200)
- `JBL_PORT`: Port of the JBL speaker (optional, default: 80)
- `JBL_PIN`: PIN of the JBL speaker (optional, default: 1234)
- `INTERVAL`: Interval in seconds to send keep-alive requests (optional, default: 60)

### Docker Run (without Compose)

You can also run the container directly with `docker run`:

```bash
docker build -t jbl-keeper .
docker run -d \
  --name jbl-keeper \
  --network host \
  --restart unless-stopped \
  -e JBL_ADDRESS=192.168.1.200 \
  -e PC_ADDRESS=192.168.1.100 \
  -e INTERVAL=60 \
  jbl-keeper
```

**Note:** The container uses `network_mode: host` to allow direct network access to the JBL speaker and to enable ping functionality for PC status checks.

## Usage

You can run the script manually with:

```
python3 main.py --jbl-address <JBL Playlist IP Address> [OPTIONS]
```

### Command-line Arguments

- `--pc-address`: IP address of the PC (optional). If script is running on separate machine than you can specify the PC's IP address to check if it's online to not keep the speaker on when you are not using it. If you are planning to run the script on the same machine where the JBL speaker is connected, you can ignore this option.
- `--jbl-address`: IP address of the JBL speaker (required).
- `--jbl-port`: Port of the JBL speaker (default: 80)
- `--jbl-pin`: PIN of the JBL speaker (default: 1234)
- `--interval`: Interval to send keep-alive requests in seconds (default: 60)

Example:

```
python3 main.py --pc-address 192.168.1.100 --jbl-address 192.168.1.200 --interval 120
```

## Automatic Service Setup

To automatically set up the JBL Keeper as a service, you can use the provided `setup.py` script. Run it with sudo privileges:

```
sudo python3 setup.py --jbl-address JBL_IP [OPTIONS]
```

### Setup Arguments

- `--jbl-address`: IP address of the JBL speaker (required)
- `--user`: User to run the service as (default: current user)
- Additional arguments will be passed to the main script. Get all the same options as you can use in manual mode.

Example:

```
sudo python3 setup.py --jbl-address 192.168.1.200 --pc-address 192.168.1.100 --interval 120
```

This will create and start the `jbl_keeper.service` automatically.

## How It Works

The script performs the following actions:

1. Checks if the specified PC is online (if a PC address is provided)
2. If the PC is online or no PC address is specified:
   - Checks the current mode and play status of the JBL speaker
   - If the speaker is in a non-Bluetooth/Aux mode but playing music through a cable:
     - Sets the speaker to Bluetooth/Aux mode
   - Sends a keep-alive request by setting the play state to pause
   - Prints the result of the attempt
4. Waits for the specified interval before repeating the process

## Troubleshooting

- If the script fails to communicate with the JBL speaker, ensure that the IP address and port are correct and that the speaker is connected to the same network as the machine running the script.
- If the PC status check fails, verify that the PC's IP address is correct and that it's accessible from the machine running the script.
- Check the console output for any error messages that may indicate the cause of issues.
- When changing the speaker from a non-Bluetooth/Aux Mode to Bluetooth/Aux mode, it may stop playing music if the volume is too low. If you experience unexpected music interruptions, try increasing the volume slightly.

## Contributing

Contributions to improve JBL Speaker Alive Keeper are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).