#!/bin/bash

echo "Setting up cost-saver project..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it with your Slack credentials."
fi

echo "Setup complete!"
echo "Please edit .env file with your Slack Bot Token and Channel ID"
echo "Run with: source venv/bin/activate && python src/main.py"
