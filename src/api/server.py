import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apify_client import ApifyClient
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI(title="Instagram Niche Finder API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
SEARCH_ACTOR_ID = "apify/instagram-search-scraper"

if not APIFY_TOKEN:
    print("WARNING: APIFY_TOKEN not found in .env")

client = ApifyClient(APIFY_TOKEN) if APIFY_TOKEN else None

def normalize_profile_data(item: dict) -> dict:
    """Normalizes data from different Apify actors to a consistent format."""
    # Common fields for both search and details actors
    return {
        "username": item.get("username") or item.get("ownerUsername"),
        "fullName": item.get("fullName") or item.get("ownerFullName"),
        "profilePicUrl": item.get("profilePicUrl") or item.get("ownerProfilePicUrl"),
        "biography": item.get("biography"),
        "followersCount": item.get("followersCount"),
        "postsCount": item.get("postsCount"),
        "url": item.get("url") or f"https://www.instagram.com/{item.get('username') or item.get('ownerUsername')}/"
    }

@app.get("/api/search")
async def search_instagram(keyword: str = Query(..., min_length=2), limit: int = 10):
    if not client:
        raise HTTPException(status_code=500, detail="Apify Token not configured.")
    
    run_input = {
        "search": keyword,
        "searchType": "user",
        "resultsLimit": limit
    }
    
    try:
        run = client.actor(SEARCH_ACTOR_ID).call(run_input=run_input)
        raw_results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        normalized_results = [normalize_profile_data(item) for item in raw_results]
        return {"status": "success", "data": normalized_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search-list")
async def search_from_list(limit: int = 10):
    if not client:
        raise HTTPException(status_code=500, detail="Apify Token not configured.")
    
    json_path = "profiles.json"
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="profiles.json file not found.")
        
    try:
        with open(json_path, "r") as f:
            profile_list = json.load(f)
            
        if not profile_list:
            return {"status": "success", "data": [], "message": "List is empty."}

        # Using the main instagram-scraper actor with 'details' for better profile info
        ACTOR_ID = "apify/instagram-scraper"
        run_input = {
            "directUrls": profile_list,
            "resultsLimit": limit,
            "resultsType": "details" # Changing from 'posts' to 'details'
        }
        
        run = client.actor(ACTOR_ID).call(run_input=run_input)
        raw_results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        normalized_results = [normalize_profile_data(item) for item in raw_results]
        return {"status": "success", "data": normalized_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend
# app.mount("/", StaticFiles(directory="src/web", html=True), name="web")
