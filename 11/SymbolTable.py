class SymbolTable:
    def __init__(self):
        self.class_symbol_table = {}
        self.subroutine_symbol_table = {}
        self.var_count = {
            "static" : 0,
            "field" : 0,
            "local" : 0,
            "argument" : 0
        }
        self.accepted_kinds = [
            "static",
            "field",
            "local",
            "argument"
        ]

        self.class_name = ""

    def startSubroutine(self):
        self.subroutine_symbol_table = {}
        self.var_count["local"] = 0
        self.var_count["argument"] = 0
    
    def define(self, s_name, s_type, s_kind):
        class_scope = [
            "static",
            "field"
        ]
        symbol_list = [s_type, s_kind, self.varCount(s_kind)]
        
        if (s_kind in class_scope):
            self.class_symbol_table[s_name] = symbol_list
        else:
            self.subroutine_symbol_table[s_name] = symbol_list

        if(s_kind in self.accepted_kinds):
            self.var_count[s_kind] += 1
        

    def varCount(self, kind):
        if (kind not in self.accepted_kinds):
            return None
        return self.var_count[kind]

    def kindOf(self, name):
        if(self.class_symbol_table.get(name, False)):
            return self.class_symbol_table[name][1]
        else:
            return self.subroutine_symbol_table[name][1]

    def typeOf(self, name):
        if(self.class_symbol_table.get(name, False)):
            return self.class_symbol_table[name][0]
        else:
            return self.subroutine_symbol_table[name][0]

    def indexOf(self, name):
        if(self.class_symbol_table.get(name, False)):
            return self.class_symbol_table[name][2]
        else:
            return self.subroutine_symbol_table[name][2]

    def contains(self, name):
        if (self.class_symbol_table.get(name, False)):
            return True
        elif (self.subroutine_symbol_table.get(name, False)):
            return True
        else:
            return False

    def setClassName(self, name):
        self.class_name = name
    

    def printTables(self):
        
        print(f"Class {self.class_name} scope table: ")
        for token, value in self.class_symbol_table.items():
            print(token, value)
        
        print("Subroutine scope table: ")
        for token, value in self.subroutine_symbol_table.items():
            print(token, value)
        

