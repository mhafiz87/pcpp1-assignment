import xml.etree.ElementTree as ET

def extract_suppliers(file_path):
    """
    Extracts supplier data from an XML file and prints each supplier.

    Args:
        file_path (str): Path to the XML file.

    Returns:
        None
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    for supplier in root.findall("Supplier"):
        print(supplier.text)

# Example Usage
if __name__ == "__main__":
    extract_suppliers("Training_Datasets/Day2/supplier_schedule.xml")
