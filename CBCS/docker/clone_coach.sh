#!/bin/bash

# CBCS Coach Cloning Script
# Usage: ./clone_coach.sh [COACH_ID] [PORT] [TELEGRAM_BOT_TOKEN]

COACH_ID=$1
PORT=${2:-8000}
TELEGRAM_BOT_TOKEN=$3

if [ -z "$COACH_ID" ]; then
    echo "Usage: ./clone_coach.sh <coach_id> <port> [telegram_bot_token]"
    exit 1
fi

echo "🚀 Cloning CBCS Backend for Coach: $COACH_ID on Port $PORT..."

# Create .env file for this instance
ENV_FILE=".env.$COACH_ID"
cp ../.env $ENV_FILE

# Override specific variables
echo "" >> $ENV_FILE
echo "# --- CLONE OVERRIDES ---" >> $ENV_FILE
echo "COACH_ID=$COACH_ID" >> $ENV_FILE
echo "PORT=$PORT" >> $ENV_FILE

if [ ! -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> $ENV_FILE
     echo "✅ Injected Custom Telegram Token"
fi

# Spin up the container
echo "🐳 Starting Docker Container..."
docker-compose -p "cbcs-$COACH_ID" --env-file $ENV_FILE up -d

echo "✅ Deployment Complete!"
echo "   Container: cbcs-$COACH_ID-cbcs-core-1"
echo "   Port:      $PORT"
echo "   Endpoint:  http://localhost:$PORT/docs"
