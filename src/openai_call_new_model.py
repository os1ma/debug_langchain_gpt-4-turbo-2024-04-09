import logging

from dotenv import load_dotenv
from openai import OpenAI

# logging.basicConfig(level=logging.DEBUG)

load_dotenv(override=True)

message_dicts = [
    {"content": "You are a helpful assistant", "role": "system"},
    {"content": "What's the weather like in Tokyo?", "role": "user"},
    {
        "content": None,
        "role": "assistant",
        "tool_calls": [
            {
                "index": 0,
                "id": "call_pB1GWEH1UmFVUtfd0kdaXnjH",
                "function": {
                    "arguments": '{"query":"current weather in Tokyo"}',
                    "name": "tavily_search_results_json",
                },
                "type": "function",
            }
        ],
    },
    {
        "content": "[{\"url\": \"https://www.weatherapi.com/\", \"content\": \"{'location': {'name': 'Tokyo', 'region': 'Tokyo', 'country': 'Japan', 'lat': 35.69, 'lon': 139.69, 'tz_id': 'Asia/Tokyo', 'localtime_epoch': 1712742554, 'localtime': '2024-04-10 18:49'}, 'current': {'last_updated_epoch': 1712742300, 'last_updated': '2024-04-10 18:45', 'temp_c': 14.6, 'temp_f': 58.2, 'is_day': 0, 'condition': {'text': 'Sunny', 'icon': '//cdn.weatherapi.com/weather/64x64/night/113.png', 'code': 1000}, 'wind_mph': 12.8, 'wind_kph': 20.5, 'wind_degree': 131, 'wind_dir': 'SE', 'pressure_mb': 1028.0, 'pressure_in': 30.36, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 29, 'cloud': 1, 'feelslike_c': 13.1, 'feelslike_f': 55.6, 'vis_km': 10.0, 'vis_miles': 6.0, 'uv': 4.0, 'gust_mph': 16.1, 'gust_kph': 26.0}}\"}]",
        "role": "tool",
        "tool_call_id": "call_pB1GWEH1UmFVUtfd0kdaXnjH",
    },
]

params = {
    "model": "gpt-4-turbo-2024-04-09",
    "stream": True,
    "n": 1,
    "temperature": 0.0,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "tavily_search_results_json",
                "description": "A search engine optimized for comprehensive, accurate, and trusted results. Useful for when you need to answer questions about current events. Input should be a search query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "description": "search query to look up",
                            "type": "string",
                        }
                    },
                    "required": ["query"],
                },
            },
        }
    ],
}

client = OpenAI()

with client.chat.completions.create(messages=message_dicts, **params) as response:
    for chunk in response:
        print(chunk)
