import asyncio
import os
import aiohttp

# --- Configuration ---
# Replace with your Quay instance details
QUAY_HOST = "quay315pg-quay-quay-enterprise-15370.apps.quaytest-15370.qe.devcluster.openshift.com"
QUAY_NAMESPACE = "testorg"
# Your Quay OAuth token is read from an environment variable for security
API_TOKEN = os.getenv("QUAY_TOKEN")

async def create_repo(session: aiohttp.ClientSession, repo_name: str):
    """Sends a single API request to create a repository."""
    url = f"https://{QUAY_HOST}/api/v1/repository"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "namespace": QUAY_NAMESPACE,
        "repository": repo_name,
        "visibility": "private",
        "description": f"Auto-created repository: {repo_name}",
    }

    print(f"[*] Creating repository: {repo_name}")
    try:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 201:
                print(f"[+] SUCCESS: Created {repo_name}")
            else:
                error_data = await response.json()
                print(
                    f"[!] FAILED: Could not create {repo_name}. "
                    f"Status: {response.status}, "
                    f"Error: {error_data.get('error_message', 'Unknown')}"
                )
    except aiohttp.ClientError as e:
        print(f"[!] EXCEPTION: An error occurred while creating {repo_name}: {e}")

async def main():
    """Orchestrates the creation of all repositories concurrently."""
    if not API_TOKEN:
        print("[!] ERROR: QUAY_TOKEN environment variable not set.")
        return

    # --- THIS LINE IS CHANGED ---
    # Generate repository names from myrepo001 to myrepo100
    repo_names = [f"quay316repo{i:03}" for i in range(1, 501)]

    connector = aiohttp.TCPConnector(limit=20,ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [create_repo(session, name) for name in repo_names]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
