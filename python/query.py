class Query:
    columns = None
    where = None
    condition = None

    def __init__(self, name, query):
        self.name = name
        self.query = query

    def Select(self, column):
        if self.columns is None: self.columns = []
        self.columns.append(column)
        return self

    def OuterWhere(self, where):
        if self.where is None: self.where = []
        self.where.append(where)
        return self

    def InnerWhere(self, condition):
        if self.condition is None: self.condition = []
        self.condition.append(condition)
        return self

    def GetWhereClause(where):
        result = []
        for w in where:
            if type(w) is Query:
                sub = w.ToQueryString()
                if sub.endswith(';'): sub = sub[:-1]
                result.append(f"exists (\n{sub})")
            else: result.append(f"({w})")
        
        return "\n  and ".join(result)
    
    def ToQueryString(self):

        if self.condition is not None:
            if self.query is Query:
                for c in self.condition: self.query.InnerWhere(c)
            else:
                if "@where" not in self.query: raise Exception("The query does not contain inner where clause.")
                self.query = self.query.replace("@where", Query.GetWhereClause(self.condition))
        elif self.query is not Query:
            self.query = self.query.replace("where (@where)", "")
        
        if self.columns is None and self.where is None: return self.query

        result = self.query.ToQueryString() if self.query is Query else self.query.strip()
        if result.endswith(';'): result = result[:-1]

        result = f"from (\n{result}) {self.name}"

        if self.columns is None: result = "select *\n" + result
        else: 
            str = ", ".join(self.columns)
            result = f"select {str}\n{result}"

        if self.where is not None:
            result += f"\nwhere {Query.GetWhereClause(self.where)}"

        return result + '\n;'
