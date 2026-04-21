import flet as ft
import requests

def main(page: ft.Page):
    # --- Window Settings ---
    page.title = "Live Crypto Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 450
    page.window.height = 700
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- Main Title ---
    page.add(
        ft.Text("CRYPTO DASHBOARD", size=24, weight=ft.FontWeight.BOLD, color="blue400"),
        ft.Divider(height=10, color="white24")
    )

    # --- Scrollable List Container ---
    # This column will hold all our dynamically generated coin rows
    crypto_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)

    # --- API Logic ---
    def fetch_crypto_data(e=None):
        # Update UI to show loading state
        refresh_btn.content = ft.Text("Loading...", size=20)
        refresh_btn.disabled = True
        crypto_list.controls.clear()
        page.update()

        try:
            # CoinGecko API endpoint for the top coins by market cap
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1,
                "sparkline": "false"
            }
            
            response = requests.get(url, params=params)

            # --- Rate Limit Check ---
            if response.status_code == 429:
                crypto_list.controls.append(
                    ft.Container(
                        content=ft.Text("Rate limit reached! CoinGecko restricts rapid refreshing. Please wait 60 seconds.", color="orange400", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
                        padding=20,
                        alignment=ft.Alignment(0, 0)
                    )
                )
                refresh_btn.content = ft.Text("Refresh", size=20)
                refresh_btn.disabled = False
                page.update()
                return # Stop processing
            
            # Raise an error for any other bad HTTP responses
            response.raise_for_status()
            
            data = response.json()

            # Loop through the JSON array and build a UI row for each coin
            for coin in data:
                name = coin["name"]
                symbol = coin["symbol"].upper()
                price = coin["current_price"]
                change_24h = coin["price_change_percentage_24h"]
                image_url = coin["image"]

                # Determine the color and arrow based on if the coin is up or down
                if change_24h > 0:
                    change_color = "green400"
                    change_text = f"▲ {change_24h:.2f}%"
                else:
                    change_color = "red400"
                    change_text = f"▼ {abs(change_24h):.2f}%"

                # Build the Glassmorphism card for this specific coin
                coin_row = ft.Container(
                    content=ft.Row(
                        [
                            # Left side: Image and Name/Symbol
                            ft.Row([
                                ft.Image(src=image_url, width=35, height=35),
                                ft.Column([
                                    ft.Text(name, weight=ft.FontWeight.BOLD, size=16),
                                    ft.Text(symbol, color="white54", size=12),
                                ], spacing=0)
                            ], spacing=15),
                            
                            # Right side: Price and 24h Change
                            ft.Column([
                                ft.Text(f"${price:,.2f}", weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(change_text, color=change_color, size=14, weight=ft.FontWeight.BOLD),
                            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.END)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=15,
                    bgcolor="#0DFFFFFF",
                    border_radius=15,
                    border=ft.Border.all(1, "#1AFFFFFF")
                )
                
                # Add the finished row to our list
                crypto_list.controls.append(coin_row)

        except Exception as ex:
            # Fallback for actual connection drops or severe API issues
            crypto_list.controls.append(
                ft.Container(
                    content=ft.Text("⚠️ Could not connect to CoinGecko. Check your internet.", color="red400", text_align=ft.TextAlign.CENTER),
                    padding=20,
                    alignment=ft.Alignment(0, 0)
                )
            )

        # Restore the refresh button icon and re-enable it
        refresh_btn.content = ft.Text("Refresh", size=20)
        refresh_btn.disabled = False
        page.update()

    # --- UI Controls ---
    # Custom Container Button for refreshing data
    refresh_btn = ft.Container(
        content=ft.Text("Refresh", size=20),
        on_click=fetch_crypto_data,
        padding=10,
        border_radius=50, 
        ink=True, 
        bgcolor="#1AFFFFFF",
        alignment=ft.Alignment(0, 0)
    )

    # A header row organizing the list title and the refresh button
    header_row = ft.Row(
        [
            ft.Text("Top 10 Cryptocurrencies", size=18, weight=ft.FontWeight.W_500, color="white70"), 
            refresh_btn
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # --- Build Page ---
    page.add(
        header_row, 
        crypto_list
    )
    
    # Automatically fetch data the moment the app opens
    fetch_crypto_data()

if hasattr(ft, 'run'):
    ft.run(main)
else:
    ft.app(target=main)