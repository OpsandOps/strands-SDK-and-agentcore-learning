import requests 

def get_location():
    """
    fetch the given location using https://www.ipapi.co accurately
    using the request library
    """
   
    base_url = "https://ipapi.co/json/"
    try:
        with requests.Session() as session:
            response = session.get(base_url, headers={"User-agent": "weather-bot 1.0"})
            data = response.json()

        return {
            "ip": data.get("ip"),
            "city": data.get("city"),
            "country_name": data.get("country_name")
        }
    except requests.RequestException as error:
        print(f"Error fetching IP location: {error}")
        return None
        

if __name__ == '__main__':
    print(f"the location is {get_location()}")