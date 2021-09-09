class ResponseSingle():
    data = {}
    schema = None

    def __init__(self, data: object, schema):
        self.data = data
        self.schema = schema
    
    def render(self):
        return self.schema.dump(self.data)