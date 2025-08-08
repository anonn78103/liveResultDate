#!/usr/bin/env bash

# Install latest Chrome for Linux
apt-get update && apt-get install -y wget gnupg unzip curl
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb || apt --fix-broken install -y
