import requests

API_KEY = ("your_yelp_api_key_here")  # Replace with your Yelp API key
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
REVIEWS_URL = "https://api.yelp.com/v3/businesses/{id}/reviews"

KEYWORDS = ["gym", "fitness", "treadmill", "workout", "fitness center", "exercise room"]

def search_hotels_with_gyms(location="New York", max_results=200):
    gathered = 0
    offset = 0
    page_size = 50

    while gathered < max_results:
        params = {
            "term": "hotel",
            "location": location,
            "categories": "hotels",
            "limit": page_size,
            "offset": offset,
            "sort_by": "rating"
        }

        resp = requests.get(SEARCH_URL, headers=HEADERS, params=params)
        if resp.status_code != 200:
            print("Yelp error:", resp.json())
            break

        businesses = resp.json().get("businesses", [])
        if not businesses:
            break

        for biz in businesses:
            r = requests.get(REVIEWS_URL.format(id=biz["id"]), headers=HEADERS)
            if r.status_code != 200:
                continue
            reviews = r.json().get("reviews", [])

            hits = [rv for rv in reviews
                    if any(kw in rv["text"].lower() for kw in KEYWORDS)]

            if hits:
                print(f"\nHotel: {biz['name']}  |  Rating: {biz['rating']}★")
                print("Address:", ", ".join(biz["location"]["display_address"]))
                print("Yelp URL:", biz["url"])

                for rv in hits:
                    print(f"Reviewer {rv['user']['name']}: {rv['text']}")
                    print("Full review:", rv["url"])
                    print("-" * 60)

        gathered += len(businesses)
        offset += page_size
        if len(businesses) < page_size:
            break


# Example
search_hotels_with_gyms("20171", max_results=150)