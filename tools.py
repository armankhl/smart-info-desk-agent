# tools.py
import os
import requests

# --- Tool 1: Weather ---
def get_weather(location: str) -> str:
    """Fetches the current weather for a given location."""
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        # Check if the API returned a valid response
        if 'weather' not in data or 'main' not in data:
            return f"Sorry, I couldn't retrieve weather data for {location}."

        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"The current weather in {location} is {temp}°C with {weather_desc}."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except KeyError:
        return f"Could not parse weather data for {location}. Please check the location name."

# --- Tool 2: News ---
def get_top_news(country_code: str) -> str:
    """Fetches the top news headline for a given country using its 2-letter ISO code."""
    api_key = os.environ.get("NEWSAPI_API_KEY")
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {"country": country_code, "apiKey": api_key, "pageSize": 1}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("articles"):
            article = data["articles"][0]
            title = article.get("title", "No title available")
            source = article.get("source", {}).get("name", "Unknown source")
            return f"Top news from {country_code.upper()}: '{title}' (Source: {source})"
        else:
            return f"Sorry, I couldn't find any top news for {country_code.upper()}."
    except requests.exceptions.RequestException as e:
        return f"Error fetching news data: {e}"

# --- Tool 3: Cryptocurrency Price ---
def get_crypto_price(coin_id: str) -> str:
    """Fetches the current price of a cryptocurrency in USD using its CoinGecko ID."""
    base_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin_id.lower(), "vs_currencies": "usd"}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if coin_id.lower() in data and 'usd' in data[coin_id.lower()]:
            price = data[coin_id.lower()]['usd']
            return f"The current price of {coin_id} is ${price:,.2f} USD."
        else:
            return f"Sorry, I couldn't find the price for the cryptocurrency ID '{coin_id}'."
    except requests.exceptions.RequestException as e:
        return f"Error fetching crypto price: {e}"

# --- Tool 4: Movie Summary ---
def get_movie_summary(title: str) -> str:
    """Fetches a brief summary of a movie by its title."""
    api_key = os.environ.get("TMDB_API_KEY")
    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": api_key, "query": title}

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            movie = data["results"][0]
            movie_title = movie.get("title", "N/A")
            overview = movie.get("overview", "No summary available.")
            return f"Summary for '{movie_title}': {overview}"
        else:
            return f"Sorry, I couldn't find a movie with the title '{title}'."
    except requests.exceptions.RequestException as e:
        return f"Error fetching movie data: {e}"