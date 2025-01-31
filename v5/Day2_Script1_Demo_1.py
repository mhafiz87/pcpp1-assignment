import xml.etree.ElementTree as ET

def parse_supplier_schedule(file_path):
    """
    Parses the supplier schedule XML file and prints each supplier ID.

    Args:
        file_path (str): Path to the XML file.

    Returns:
        None
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    for schedule in root.findall("Schedule"):
        supplier_id = schedule.find("Supplier_ID").text
        print(f"Supplier ID: {supplier_id}")

# Example Usage
if __name__ == "__main__":
    parse_supplier_schedule("Training_Datasets/Day2/supplier_schedule.xml")
