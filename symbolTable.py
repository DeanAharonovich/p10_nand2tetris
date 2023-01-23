class SymbolTable:
    # variable kinds
    ARG = "argument"
    LOCAL = "var"
    STATIC = "static"
    FIELD = "field"

    # Each symbol table (class,subroutine) is represented as a different instances
    def __init__(self):
        self.subroutine_var_dec = {}
        self.class_var_dec = {}
        self.argument_index = 0
        self.local_index = 0
        self.static_index = 0
        self.field_index = 0
        self.class_name = None
        self.methods = set()
        self.while_counter = 0

    # def reset(self):
    #     self.subroutine_var_dec = []
    #     self.class_var_dec = []
    #     self.argument_index = 0
    #     self.local_index = 0
    #     self.static_index = 0
    #     self.field_index = 0

    def define(self, name, type, kind):
        if kind == SymbolTable.ARG or kind == SymbolTable.LOCAL:
            if kind == SymbolTable.ARG:
                self.subroutine_var_dec[name] = {"type": type, "kind": kind, "index": self.argument_index}
                self.argument_index += 1
            if kind == SymbolTable.LOCAL:
                self.subroutine_var_dec[name] = {"type": type, "kind": "local", "index": self.local_index}
                self.local_index += 1
        else:
            if kind == SymbolTable.STATIC:
                self.class_var_dec[name] = {"type": type, "kind": "constant", "index": self.static_index}
                self.static_index += 1
            if kind == SymbolTable.FIELD:
                self.class_var_dec[name] = {"type": type, "kind": "this", "index": self.field_index}
                self.field_index += 1
    def reset_subroutine(self):
        self.subroutine_var_dec = {}
        self.argument_index = 0 
        self.local_index = 0 
        
    def var_count(self, kind):
        return getattr(self, "{}_index".format(kind))

    def kind_of(self, name):
        return self.get_var(name)["kind"]

    def type_of(self, name):
        return self.get_var(name)["type"]

    def index_of(self, name):
        return self.get_var(name)["index"]

    def get_var(self, name):
        return self.subroutine_var_dec.get(name, self.class_var_dec.get(name, None))
