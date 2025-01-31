import json
import xml.etree.ElementTree as ET

def merge_data(xml_file, json_file, output_file):
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    suppliers = [
        {"Supplier_ID": schedule.find("Supplier_ID").text,
         "Material_Type": schedule.find("Material_Type").text,
         "Delivery_Date": schedule.find("Delivery_Date").text}
        for schedule in root.findall("Schedule")
    ]

    # Parse JSON
    with open(json_file, mode="r") as infile:
        inventory = json.load(infile)

    # Combine Data
    combined_data = {
        "Suppliers": suppliers,
        "Inventory": inventory
    }

    # Save Combined Data
    with open(output_file, mode="w") as outfile:
        json.dump(combined_data, outfile, indent=4)

# Example Usage
if __name__ == "__main__":
    merge_data(
        "Training_Datasets/Day3/supplier_schedule.xml",
        "filtered_inventory.json",
        "combined_data.json"
    )
    print("Combined data saved to combined_data.json.")
