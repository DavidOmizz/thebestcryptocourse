# from django.conf import settings

# # Static ticker content for the scrolling bar at the very top of the site.
# # Format: (label, change_text, direction) -- direction is "up", "down", or "" for plain text.
# # This is intentionally not database-backed to keep Phase 1 simple; if you
# # want this editable from /admin/ later, it can become a small model.
# # TICKER_ITEMS = [
# #     ("BTC", "\u25B2 2.4%", "up"),
# #     ("ETH", "\u25B2 1.1%", "up"),
# #     ("New lesson published: \"Reading Order Books\"", "", ""),
# #     ("SOL", "\u25BC 0.8%", "down"),
# #     ("12 traders started \"Technical Analysis Masterclass\" this week", "", ""),
# # ]


# TICKER_COINS = [
#     "BTCUSDT",
#     "ETHUSDT",
#     "BNBUSDT",
#     "SOLUSDT",
#     "XRPUSDT",
#     "ADAUSDT",
# ]
# # def site_settings(request):
# #     """Makes {{ site_name }} and {{ ticker_items }} available in every template."""
# #     return {
# #         "site_name": settings.SITE_NAME,
# #         "ticker_items": TICKER_ITEMS,
# #     }


# import requests

# def site_settings(request):

#     ticker_items = []

#     try:

#         response = requests.get(
#             "https://api.binance.com/api/v3/ticker/24hr",
#             params={
#                 "symbols": '["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT"]'
#             },
#             timeout=5
#         )

#         data = response.json()

#         for coin in data:

#             symbol = coin["symbol"].replace("USDT", "")

#             change = float(coin["priceChangePercent"])

#             if change >= 0:
#                 direction = "up"
#                 value = f"▲ {change:.2f}%"
#             else:
#                 direction = "down"
#                 value = f"▼ {abs(change):.2f}%"

#             ticker_items.append(
#                 (symbol, value, direction)
#             )

#     except Exception:

#         # Fallback if Binance is unavailable
#         ticker_items = [
#             ("BTC", "▲ --", "up"),
#             ("ETH", "▲ --", "up"),
#             ("BNB", "▲ --", "up"),
#             ("SOL", "▲ --", "up"),
#             ("XRP", "▲ --", "up"),
#             ("ADA", "▲ --", "up"),
#         ]

#     return {
#         "site_name": settings.SITE_NAME,
#         "ticker_items": ticker_items,
#     }




# This works but Production is not working because of the Binance API. I will comment out the code and use static data for now. I will fix it later.


# from django.conf import settings
# import requests


# TICKER_COINS = [
#     "BTCUSDT",
#     "ETHUSDT",
#     "BNBUSDT",
#     "SOLUSDT",
#     "XRPUSDT",
#     "ADAUSDT",
#     "DOGEUSDT",
#     "AVAXUSDT",
#     "LINKUSDT",
#     "DOTUSDT",
# ]


# def site_settings(request):

#     ticker_items = []

#     try:

#         response = requests.get(
#             "https://api.binance.com/api/v3/ticker/24hr",
#             params={
#                 "symbols": '["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT","DOGEUSDT","AVAXUSDT","LINKUSDT","DOTUSDT"]'
#             },
#             timeout=5
#         )

#         response.raise_for_status()

#         data = response.json()

#         for coin in data:

#             symbol = coin["symbol"].replace("USDT", "")

#             change = float(coin["priceChangePercent"])

#             if change >= 0:
#                 direction = "up"
#                 value = f"▲ {change:.2f}%"
#             else:
#                 direction = "down"
#                 value = f"▼ {abs(change):.2f}%"

#             ticker_items.append(
#                 (symbol, value, direction)
#             )

#     except Exception as e:

#         print("BINANCE TICKER ERROR:", e)

#         ticker_items = [
#             ("BTC", "▲ --", "up"),
#             ("ETH", "▲ --", "up"),
#             ("BNB", "▲ --", "up"),
#             ("SOL", "▲ --", "up"),
#             ("XRP", "▲ --", "up"),
#             ("ADA", "▲ --", "up"),
#             ("DOGE", "▲ --", "up"),
#             ("AVAX", "▲ --", "up"),
#             ("LINK", "▲ --", "up"),
#             ("DOT", "▲ --", "up"),
#         ]

#     return {
#         "site_name": settings.SITE_NAME,
#         "ticker_items": ticker_items,
#     }



from django.conf import settings
import requests


TICKER_COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "binancecoin": "BNB",
    "solana": "SOL",
    "ripple": "XRP",
    "cardano": "ADA",
    "dogecoin": "DOGE",
    "avalanche-2": "AVAX",
    "chainlink": "LINK",
    "polkadot": "DOT",
}


def site_settings(request):

    ticker_items = []

    try:

        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "ids": ",".join(TICKER_COINS.keys()),
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1,
                "sparkline": "false",
                "price_change_percentage": "24h",
                # "x_cg_demo_api_key": settings.COINGECKO_API_KEY,
                "x_cg_demo_api_key": "CG-p5CMZHkc8RnahpTRxMTpFNB9",
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        for coin in data:

            symbol = TICKER_COINS.get(coin["id"])

            if not symbol:
                continue

            change = coin.get("price_change_percentage_24h")

            if change is None:
                continue

            change = float(change)

            if change >= 0:
                direction = "up"
                value = f"▲ {change:.2f}%"
            else:
                direction = "down"
                value = f"▼ {abs(change):.2f}%"

            ticker_items.append(
                (symbol, value, direction)
            )

    except Exception as e:

        print("COINGECKO TICKER ERROR:", e)

        ticker_items = [
            ("BTC", "▲ --", "up"),
            ("ETH", "▲ --", "up"),
            ("BNB", "▲ --", "up"),
            ("SOL", "▲ --", "up"),
            ("XRP", "▲ --", "up"),
            ("ADA", "▲ --", "up"),
            ("DOGE", "▲ --", "up"),
            ("AVAX", "▲ --", "up"),
            ("LINK", "▲ --", "up"),
            ("DOT", "▲ --", "up"),
        ]

    return {
        "site_name": settings.SITE_NAME,
        "ticker_items": ticker_items,
    }