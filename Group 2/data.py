import json
import csv
import sqlite3
from datetime import datetime

PRODUCTION_DATA_PATH = r"training\data_set\production_data.csv"
PRODUCTION_DATA_DB = r"training\data_set\production_data.db"
MACHINE_DATA_PATH = r"training\data_set\machine_data.json"


class ProductionData:
    def __init__(self):
        self.__machine_data = {}
        self.__data_table = []
        self.init_db()

    @property
    def machine_data(self) -> dict[str, str]:
        if not self.__machine_data:
            self.__machine_data = json.load(open(MACHINE_DATA_PATH))
        return self.__machine_data

    @property
    def machine_list(self) -> list[str]:
        return list(self.machine_data.values())

    @property
    def product_list(self) -> list[str]:
        return list(self.machine_data.keys())

    @property
    def production_data(self) -> list[dict[str, str]]:
        if not self.__data_table:
            self.cursor.execute("SELECT * FROM ProductionData")
            db_data: list[tuple] = self.cursor.fetchall()
            keys = (
                "batch_id",
                "machine_id",
                "machine_type",
                "product_id",
                "start_date",
                "end_date",
                "units",
                "result",
                "remarks",
            )
            for db_row in db_data:
                data_dict = dict(zip(keys, db_row))
                product_id = data_dict.pop("product_id")
                self.cursor.execute(
                    f"SELECT DISTINCT * FROM Product WHERE product_id in (?)",
                    (product_id,),
                )
                _, product_type = self.cursor.fetchone()
                data_dict["product_type"] = product_type
                self.__data_table.append(data_dict)
        return self.__data_table

    def init_db(self):
        self.conn = sqlite3.connect(PRODUCTION_DATA_DB)
        self.cursor = self.conn.cursor()

        # Create Machine table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Machine (
                machine_id TEXT PRIMARY KEY,
                machine_type TEXT NOT NULL
            )
            """
        )

        # Create Product table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Product (
                product_id TEXT PRIMARY KEY,
                product_type TEXT NOT NULL
            )
            """
        )

        # Create ProductionData table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ProductionData (
                batch_id TEXT PRIMARY KEY,
                machine_id TEXT NOT NULL,
                machine_type TEXT NOT NULL,
                product_id TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                units INTEGER NOT NULL,
                result TEXT,
                remarks TEXT,
                FOREIGN KEY (machine_id) REFERENCES Machine (machine_id),
                FOREIGN KEY (product_id) REFERENCES Product (product_id)
            )
            """
        )

        self.conn.commit()

    def add_data(self, payload_dict: dict) -> tuple[bool, str]:
        batch_id = payload_dict.get("batch_id", "")
        machine_id = payload_dict.get("machine_id", "")
        machine_type = payload_dict.get("machine_type", "")
        product_type = payload_dict.get("product_type", "")
        start_date = payload_dict.get("start_date", "")
        end_date = payload_dict.get("end_date", "")
        units = payload_dict.get("units", "")
        result = payload_dict.get("result", "")
        remarks = payload_dict.get("remarks", "")
        if not self.validate_date(date_input=start_date):
            return False, f"Date: {start_date} is not valid!"
        if not self.is_machine_n_product_match(
            machine=machine_type, product=product_type
        ):
            return (
                False,
                f"Machine type: {machine_type} does not match product type: {product_type}!",
            )
        if self.check_data_exists(batch_id=batch_id):
            return False, f"Data for batch ID: {batch_id} already exists!"
        new_data_row = {
            "batch_id": batch_id,
            "machine_id": machine_id,
            "machine_type": machine_type,
            "product_type": product_type,
            "start_date": start_date,
            "end_date": end_date,
            "units": units,
            "result": result,
            "remarks": remarks,
        }
        self.__data_table.append(new_data_row)
        self.cursor.execute(
            f"SELECT DISTINCT * FROM Product WHERE product_type in (?)", (product_type,)
        )
        product_id, _ = self.cursor.fetchone()
        new_data_row.pop("product_type")
        new_data_row["product_id"] = product_id
        placeholders = ", ".join(["?" for _ in new_data_row])
        column_names = ", ".join([key for key in new_data_row.keys()])
        self.cursor.execute(
            f"INSERT INTO ProductionData ({column_names}) VALUES ({placeholders})",
            tuple(new_data_row.values()),
        )
        self.conn.commit()
        return True, f"New data, batch ID: {batch_id}, has been added"

    def update_result(self, payload_dict: dict) -> tuple[bool, str]:
        batch_id = payload_dict.get("batch_id", "")
        result = payload_dict.get("result", "")
        remarks = payload_dict.get("remarks", "")
        if not self.check_data_exists(batch_id=batch_id):
            return False, f"Batch ID: {batch_id} does not exists!"
        if not result:
            return False, "Result field must not be empty!"
        if result == "fail" and not remarks:
            return False, f"Please add remarks of why Batch ID: {batch_id} failed"
        for data_row in self.__data_table:
            if batch_id != data_row["batch_id"]:
                continue
            data_row["result"] = result
            data_row["remarks"] = remarks
            break
        self.cursor.execute(
            "UPDATE ProductionData SET result = ?, remarks = ?  WHERE batch_id = ?",
            (result, remarks, batch_id),
        )
        self.conn.commit()
        return True, f"Inspection result for Batch ID: {batch_id} has been updated"

    def delete_data_row(self, payload_dict: dict) -> tuple[bool, str]:
        batch_id = payload_dict.get("batch_id", "")
        if not batch_id:
            return False, "Please provide batch_id to be deleted"
        if not self.check_data_exists(batch_id=batch_id):
            return False, f"Batch ID: {batch_id} does not exists!"
        self.cursor.execute(
            "DELETE FROM ProductionData WHERE batch_id = ?", (batch_id,)
        )
        self.conn.commit()
        return True, f"Batch ID: {batch_id} data has been deleted"

    @staticmethod
    def validate_date(date_input: str) -> bool:
        is_valid = False
        try:
            datetime.strptime(date_input, "%d/%m/%Y")
            is_valid = True
        except ValueError as e:
            print(f"ValueError occurred: {e.args}")
        except Exception as e:
            print("Unknown error occurred!")

        return is_valid

    def get_column_values(self, column_name: str) -> list[str]:
        return list({data_row[column_name] for data_row in self.production_data})

    def filter_data(
        self, column_name: str = "", value: str = ""
    ) -> list[dict[str, str]]:
        if not column_name and not value:
            return self.production_data
        return [
            data_row
            for data_row in self.production_data
            if data_row[column_name] == value
        ]

    def is_machine_n_product_match(self, machine: str, product: str) -> bool:
        return self.machine_data[product] == machine

    def check_data_exists(self, batch_id: str) -> bool:
        return any(
            [batch_id == data_dict["batch_id"] for data_dict in self.__data_table]
        )


if __name__ == "__main__":
    prod_data = ProductionData()
    print(prod_data.production_data)
    # machines = [
    #     ("mch_spk_001", "speaker assembly machine"),
    #     ("mch_hph_001", "headphones assembly machine"),
    #     ("mch_tv_001", "tv assembly machine"),
    #     ("mch_spk_002", "speaker assembly machine"),
    #     ("mch_hph_002", "headphones assembly machine"),
    #     ("mch_tv_002", "tv assembly machine"),
    # ]
    # prod_data.cursor.executemany(
    #     "INSERT INTO Machine (machine_id, machine_type) VALUES (?,?)", machines
    # )

    # products = [
    #     ("prod_001", "speaker"),
    #     ("prod_002", "headphones"),
    #     ("prod_003", "tv"),
    # ]
    # prod_data.cursor.executemany(
    #     "INSERT INTO Product (product_id, product_type) VALUES (?,?)", products
    # )

    # data = [
    #     (
    #         "spk_001",
    #         "mch_spk_001",
    #         "speaker assembly machine",
    #         "prod_001",
    #         "1/1/2024",
    #         "8/1/2024",
    #         700,
    #         "pass",
    #         "",
    #     ),
    #     (
    #         "hph_001",
    #         "mch_hph_001",
    #         "headphones assembly machine",
    #         "prod_002",
    #         "13/1/2024",
    #         "31/1/2024",
    #         180,
    #         "pass",
    #         "",
    #     ),
    #     (
    #         "tv_001",
    #         "mch_tv_001",
    #         "tv assembly machine",
    #         "prod_003",
    #         "25/7/2024",
    #         "31/10/2024",
    #         1200,
    #         "pass",
    #         "",
    #     ),
    #     (
    #         "spk_002",
    #         "mch_spk_002",
    #         "speaker assembly machine",
    #         "prod_001",
    #         "12/1/2024",
    #         "19/1/2024",
    #         700,
    #         "fail",
    #         "50 units have missing tweeters",
    #     ),
    #     (
    #         "hph_002",
    #         "mch_hph_002",
    #         "headphones assembly machine",
    #         "prod_002",
    #         "13/2/2024",
    #         "31/3/2024",
    #         200,
    #         "pass",
    #         "",
    #     ),
    #     (
    #         "tv_002",
    #         "mch_tv_002",
    #         "tv assembly machine",
    #         "prod_003",
    #         "25/11/2024",
    #         "31/3/2025",
    #         1200,
    #         "",
    #         "",
    #     ),
    # ]
    # prod_data.cursor.executemany(
    #     "INSERT INTO ProductionData (batch_id, machine_id, machine_type, product_id, start_date, end_date, units, result, remarks) VALUES (?,?,?,?,?,?,?,?,?)",
    #     data,
    # )

    # prod_data.conn.commit()
