import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

class InstagramApifyClient:
    def __init__(self):
        self.token = os.getenv("APIFY_TOKEN")
        self.actor_id = os.getenv("APIFY_ACTOR_ID", "apify/instagram-scraper")
        if not self.token:
            raise ValueError("APIFY_TOKEN not found in environment variables.")
        self.client = ApifyClient(self.token)

    def scrape_profile(self, profile_url, results_limit=10):
        """
        Runs the Apify Instagram Scraper actor for a specific profile.
        """
        run_input = {
            "directUrls": [profile_url],
            "resultsLimit": results_limit,
            "scrapeType": "posts"
        }

        print(f"Starting Apify run for: {profile_url}...")
        run = self.client.actor(self.actor_id).call(run_input=run_input)

        print(f"Run finished. Fetching results from dataset: {run['defaultDatasetId']}")
        return list(self.client.dataset(run["defaultDatasetId"]).iterate_items())

if __name__ == "__main__":
    # Test block
    try:
        scraper = InstagramApifyClient()
        # example_url = "https://www.instagram.com/instagram/"
        # results = scraper.scrape_profile(example_url)
        # print(results)
    except Exception as e:
        print(f"Error: {e}")
