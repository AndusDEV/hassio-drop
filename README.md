# Andus Home Assistant Integrations

## Installation
_(Requires HACS installed)_

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=AndusDEV&repository=hassio-integrations)

## Important Notes
- This integration uses admin API Token
    - To get the API Token, go to Drop, open `Admin Dashboard` > `Settings` > `API tokens`, and generate a token with: **library:read**, **user:read**, **news:read**

## Configuration
1. Go to `Settings` > `Devices & Services` > `Add Integration` > Search "Drop"
2. Enter your Drop server base URL (e.g., http://192.168.1.123:3000)
3. Enter your API token

## Features

This integration connects to your self-hosted [**Drop server**](https://droposs.org/) and exposes sensors for:
- Number of games
- Number of users
- Latest added game

### Future Features (When/If Drop Supports Them)

- **News (already in Drop):** shows news feed from Drop
- **User Activity/Presence:**
    - "Andus playing Cat Quest II"
    - "Andus online"
    - "Andus offline"
- **Curently playing:** "X users currently playing"