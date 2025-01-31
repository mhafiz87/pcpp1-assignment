import requests

def fetch_and_filter_inventory(threshold):
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    if response.status_code == 200:
        items = response.json()
        filtered_items = [item for item in items if item["userId"] < threshold]
        print("Filtered Items:")
        for item in filtered_items:
            print(item)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# Example Usage
if __name__ == "__main__":
    fetch_and_filter_inventory(3)
