class SymbolTable:
    def __init__(self):
        self.table = {}
        self.base_address = 1000

    def insert(self, name, token_type, line):
        if name in self.table:
            return False, f"Symbol '{name}' already exists in Symbol Table."
        
        # Determine data type and scope based on MyC-Lite rules
        scope = "Global"
        if name.startswith("c_"):
            data_type = "Constant Identifier"
        elif name.startswith("fn_"):
            data_type = "Function"
        else:
            data_type = "Variable"
            
        address = self.base_address + (len(self.table) * 4)
        
        self.table[name] = {
            "name": name,
            "type": data_type,
            "scope": scope,
            "address": address,
            "line": line,
            "reason": f"Inserted valid MyC-Lite structural entity '{name}' declared on line {line}."
        }
        return True, f"Successfully allocated storage at address {address}."

    def get_all(self):
        return list(self.table.values())