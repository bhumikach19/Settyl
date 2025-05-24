import pandas as pd
import re

class HSNValidator:
    def __init__(self, excel_path):
        self.hsn_data = self._load_data(excel_path)
        self.hsn_data.columns = self.hsn_data.columns.str.strip()  # Strip column names
        print("Columns found in Excel:", self.hsn_data.columns.tolist())  
        if 'HSNCode' not in self.hsn_data.columns or 'Description' not in self.hsn_data.columns:
           raise ValueError("Excel file must contain 'HSNCode' and 'Description' columns.")
        self.valid_codes = set(self.hsn_data['HSNCode'].astype(str))


    def _load_data(self, path):
        return pd.read_excel(path, engine='openpyxl')

    def is_valid_format(self, hsn_code):
        #Validates if HSN code is numeric and 2 to 8 digits long.
        return bool(re.fullmatch(r'\d{2,8}', hsn_code))

    def exists_in_master(self, hsn_code):
        #Checks if the HSN code exists in the master data.
        return hsn_code in self.valid_codes

    def validate_code(self, hsn_code, hierarchical=False):
        #Validates a single HSN code.
        hsn_code = str(hsn_code).strip()
        result = {"code": hsn_code}

        if not self.is_valid_format(hsn_code):
            result.update({
                "valid": False,
                "reason": "Invalid format. HSN codes must be numeric and 2-8 digits long."
            })
        elif not self.exists_in_master(hsn_code):
            result.update({
                "valid": False,
                "reason": "Code not found in master data."
            })
        else:
            result.update({
                "valid": True,
                "description": self.hsn_data.loc[self.hsn_data['HSNCode'].astype(str) == hsn_code, 'Description'].values[0]
            })
            if hierarchical:
                result["hierarchy"] = self.get_parent_codes(hsn_code)

        return result

    def get_parent_codes(self, hsn_code):
        #Returns existing parent HSN codes for a valid HSN code.
        parents = []
        for length in [2, 4, 6]:
            if len(hsn_code) > length:
                prefix = hsn_code[:length]
                if prefix in self.valid_codes:
                    parents.append({
                        "code": prefix,
                        "description": self.hsn_data.loc[self.hsn_data['HSNCode'].astype(str) == prefix, 'Description'].values[0]
                    })
        return parents

    def validate_multiple(self, codes, hierarchical=False):
        return [self.validate_code(code, hierarchical=hierarchical) for code in codes]


# --- Example Usage ---
if __name__ == "__main__":
    validator = HSNValidator(r"C:\Users\BHUMIKA\Desktop\Settyl\HSN_SAC.xlsx")
    
    while True:
        user_input = input("Enter HSN code(s) separated by commas (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        codes = [code.strip() for code in user_input.split(",")]
        results = validator.validate_multiple(codes, hierarchical=True)

        for res in results:
            print(res)
