import requests

def search_web(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get('Abstract', 'No results found')
    return "Search failed"
