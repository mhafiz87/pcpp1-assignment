def extract_suppliers(filepath):tree=ET.parse(filepath);root=tree.getroot();for s in root.findall("Supplier"):print(s)
