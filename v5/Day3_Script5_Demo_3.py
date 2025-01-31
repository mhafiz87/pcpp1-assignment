import csv

def filter_high_production_machines(input_file, output_file, threshold):
    with open(input_file, mode="r") as infile, open(output_file, mode="w", newline="") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if int(row["Units_Produced"]) > threshold:
                writer.writerow(row)

# Example Usage
if __name__ == "__main__":
    filter_high_production_machines(
        "Training_Datasets/Day1/production_line_data.csv",
        "high_production_machines.csv",
        300
    )
    print("Filtered machines saved to high_production_machines.csv.")
