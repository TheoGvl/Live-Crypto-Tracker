# Live Crypto Tracker

A modern, responsive desktop financial dashboard built with Python and Flet. This application dynamically fetches and tracks real-time market data for the world's top cryptocurrencies using a completely free, open API.

Note: The application will automatically fetch the latest data upon launch. You can click the circular refresh button at any time to pull new market data, but please wait ~60 seconds between manual refreshes to respect the public API limits.

## Features

* **Real-Time Market Data:** Tracks current prices and 24-hour percentage changes for the top 10 cryptocurrencies by market cap.
* **Smart Rate-Limit Handling:** Automatically detects API throttling (HTTP 429) and provides user-friendly UI feedback instead of crashing, preventing accidental IP bans.
* **Dynamic Media Loading:** Uses Flet's `Image` control to asynchronously download and render the official PNG logos for each network on the fly.
* **Smart Number Formatting:** Automatically formats large currency values with thousands separators for professional readability.

## Privacy & Data Security

This application is built with an architecture that prioritizes user privacy and security:

* **Keyless API Integration:** Powered by the open [CoinGecko API](https://www.coingecko.com/en/api). It requires zero API keys, secret tokens, or user authentication to function.
* **Zero Tracking:** The app does not collect, store, or transmit any personal data, local files, or geolocation data. The only information sent over the network is the strict HTTP request for generic market data.
* **Safe to Share:** Because it relies entirely on public endpoints without embedded credentials, you can safely share this source code with anyone, or host it publicly on GitHub, without any risk of exposing private information or incurring API usage costs.

## Prerequisites

Ensure you have **Python 3.8+** installed on your system. 

You will need the Flet framework and the `requests` library to handle HTTP networking:

```
pip install flet requests
```

## How to Run Locally
Clone or download this repository to your local machine.
Open your terminal or command prompt.
Navigate to the directory containing the script.
Run the application:

```
python crypto_tracker.py
