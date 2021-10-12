class ResponsePagination():
    pagination = {}
    schema = None

    def __init__(self, pagination: object, schema):
        self.pagination = pagination
        self.schema = schema
    
    def render(self):
        return {
            'meta': {
                'page': self.pagination.page,
                'pages': self.pagination.pages,
                'per_page': self.pagination.per_page,
                'total': self.pagination.total
            },
            'data': self.schema.dump(self.pagination.items, many=True)
        }