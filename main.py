import uvicorn
import os
from src.api.server import app
from fastapi.staticfiles import StaticFiles

# Mount static files for the frontend
current_dir = os.path.dirname(os.path.abspath(__file__))
web_dir = os.path.join(current_dir, "src", "web")
app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")

def main():
    print("Iniciando Servidor Niche Finder em http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
