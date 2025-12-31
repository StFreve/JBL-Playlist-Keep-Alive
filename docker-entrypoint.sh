#!/bin/bash
set -e

# Build command arguments
ARGS=()

# Add PC address if provided
if [ -n "${PC_ADDRESS}" ]; then
    ARGS+=("--pc-address" "${PC_ADDRESS}")
fi

# Add JBL address (required)
ARGS+=("--jbl-address" "${JBL_ADDRESS:-192.168.1.200}")

# Add JBL port (optional, default: 80)
if [ -n "${JBL_PORT}" ]; then
    ARGS+=("--jbl-port" "${JBL_PORT}")
fi

# Add JBL PIN (optional, default: 1234)
if [ -n "${JBL_PIN}" ]; then
    ARGS+=("--jbl-pin" "${JBL_PIN}")
fi

# Add interval (optional, default: 60)
if [ -n "${INTERVAL}" ]; then
    ARGS+=("--interval" "${INTERVAL}")
fi

# Execute the main script with all arguments
exec python main.py "${ARGS[@]}"

