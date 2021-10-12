class ResponseList():
    pagination = {}
    schema = None

    def __init__(self, data: list, schema):
        self.data = data
        self.schema = schema
    
    def render(self):
        return {
            'data': self.schema.dump(self.data, many=True)
        }