import json

def filter_inventory(input_file, output_file, threshold):
    with open(input_file, mode="r") as infile:
        inventory = json.load(infile)

    filtered_inventory = [item for item in inventory if item["Stock_Level"] < threshold]

    with open(output_file, mode="w") as outfile:
        json.dump(filtered_inventory, outfile, indent=4)

# Example Usage
if __name__ == "__main__":
    filter_inventory("Training_Datasets/Day3/inventory_levels.json", "filtered_inventory.json", 300)
    print("Filtered inventory saved to filtered_inventory.json.")
