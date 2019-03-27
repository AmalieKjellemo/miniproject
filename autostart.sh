#!/bin/sh
gcloud config set compute/zone europe-west6-c
export PROJECT_ID="$(gcloud config get-value project -q)"
docker pull cassandra:latest
docker run -p 9042:9042 --name cassandra -d cassandra:latest
echo "Installing requirements"
sudo pip install -U -r requirements.txt
leafpad
echo "Activating Flask"
source "./venv/bin/activate"
leafpad
echo "Running python"
python main.py
exec bash