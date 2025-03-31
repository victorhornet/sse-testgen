#!/bin/bash

# Confirm that the user is on macOS
echo -n "Are you running this script on macOS? (y/N): "
read -r macoscheck
if [[ ! $macoscheck =~ ^[Yy]$ ]]; then
    echo "This script is only for macOS. Exiting."
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install uv before running this script."
    exit 1
fi


# Remind the user to turn off any other applications
echo "Please turn off any other applications before proceeding"
echo "Press Enter to continue"
read -p ""

# Remind the user to turn off adaptive brightness
echo "Please turn off adaptive brightness and screen saver before proceeding. Set your brightness to a consistent level"
echo "Press Enter to continue"
read -p ""

# Store the wifi, bluetooth and sleep settings before changing
pmset -g | grep displaysleep | awk '{print $2}' > /tmp/sleep_status

# Turn off wifi, bluetooth, and any other settings that might impact the energy measurements, such as screen saver, power management, etc.
networksetup -setairportpower en0 off
pmset -a displaysleep 0

# Tell the user to turn off bluetooth, airdrop
echo "Please turn off bluetooth and airdrop before proceeding"
echo "Press Enter to continue"
read -p ""

# Ask for the number of iterations
echo -n "Enter the number of iterations (default: 10): "
read -r iterations
iterations=${iterations:-10}
echo "Will run with $iterations iterations"

# Run the experiment
if [[ "$1" == "-y" ]]; then
    run="y"
else
    echo -n "Run experiment? (y/N): "
    read -r run
fi
if [[ $run =~ ^[Yy]$ ]]; then
    time uv run python main.py --allowed-projects codetiming_local,docstring_parser_local --iterations $iterations
    echo "Experiment complete"
else
    echo "Experiment cancelled"
fi

# Revert the settings from the stored values
networksetup -setairportpower en0 on
pmset -a displaysleep $(cat /tmp/sleep_status)

# Remind the user to turn on adaptive brightness
echo "Don't forget to turn back on adaptive brightness, bluetooth, and airdrop, etc."
echo "Press Enter to continue"
read -p ""
