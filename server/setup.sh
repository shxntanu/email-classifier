#!/bin/bash

# Function to prompt for input and set environment variables
get_input() {
    read -r -p "Enter $1: " value
    echo "$value"
}

# Function to prompt for yes/no input
get_confirmation() {
    while true; do
        read -r -p "$1 (y/n): " yn
        case $yn in
        [Yy]*)
            echo "yes"
            break
            ;;
        [Nn]*)
            echo "no"
            break
            ;;
        *) echo "Please answer yes or no." ;;
        esac
    done
}

OUTPUT_FILE="server/.env"

# Check if .env file already exists
if [ -f "$OUTPUT_FILE" ]; then
    USE_EXISTING=$(get_confirmation "Existing configuration found. Use the same?")
    if [ "$USE_EXISTING" == "yes" ]; then
        echo "Using existing configuration."
        # TODO: Start the entrypoint script from here
        exit 0
    fi
fi

# Create output environment variables file
touch server/.env

# Prompt the user for environment variables
EMAIL_ID=$(get_input "Email ID")
EMAIL_USERNAME=$(get_input "Email Username")
EMAIL_PASSWORD=$(get_input "Email Password")
GMAIL_APP_PASSWORD=$(get_input "Gmail App Password (leave blank if not using Gmail)")

TEMPLATE_FILE="server/.env.tmpl"

# Replace placeholders in the template file with the environment variables
sed -e "s/{{EMAIL_ID}}/$EMAIL_ID/" \
    -e "s/{{EMAIL_USERNAME}}/$EMAIL_USERNAME/" \
    -e "s/{{EMAIL_PASSWORD}}/$EMAIL_PASSWORD/" \
    -e "s/{{GMAIL_APP_PASSWORD}}/$GMAIL_APP_PASSWORD/" \
    $TEMPLATE_FILE >$OUTPUT_FILE

echo "Environment file $OUTPUT_FILE has been created successfully."
