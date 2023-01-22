class SymbolTable:
    # variable kinds
    ARG = "argument"
    LOCAL = "local"
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
                self.argument_index += 1
                self.subroutine_var_dec[name] = {"type": type, "kind": kind, "index": self.argument_index}
            if kind == SymbolTable.LOCAL:
                self.local_index += 1
                self.subroutine_var_dec[name] = {"type": type, "kind": kind, "index": self.local_index}
        else:
            if kind == SymbolTable.STATIC:
                self.static_index += 1
                self.class_var_dec[name] = {"type": type, "kind": kind, "index": self.static_index}
            if kind == SymbolTable.FIELD:
                self.field_index += 1
                self.class_var_dec[name] = {"type": type, "kind": kind, "index": self.static_index}

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
