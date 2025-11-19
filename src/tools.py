from langchain_core.tools import tool
import random

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    # Mock weather data
    weather_conditions = ["Sunny", "Cloudy", "Rainy", "Snowy"]
    return f"The weather in {location} is {random.choice(weather_conditions)}."

@tool
def magic_calculator(a: int, b: int) -> int:
    """A magical calculator that adds two numbers and multiplies by a random magic factor."""
    magic_factor = 2
    return (a + b) * magic_factor

