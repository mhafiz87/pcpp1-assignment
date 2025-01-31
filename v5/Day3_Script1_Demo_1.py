import requests

# Fetch data from API
def fetch_inventory():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    if response.status_code == 200:
        print("Data fetched successfully:")
        print(response.json())
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# Update data using API
def update_inventory():
    payload = {"title": "Updated Inventory", "body": "Updated data for inventory.", "userId": 1}
    response = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=payload)
    if response.status_code == 200:
        print("Data updated successfully:")
        print(response.json())
    else:
        print(f"Failed to update data. Status code: {response.status_code}")

# Example Usage
if __name__ == "__main__":
    fetch_inventory()
    update_inventory()
