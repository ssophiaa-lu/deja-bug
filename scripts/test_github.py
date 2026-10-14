import os, requests
from dotenv import load_dotenv
load_dotenv()
r = requests.get("https://api.github.com/rate_limit",
                 headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"})
print(r.json()["resources"]["core"])