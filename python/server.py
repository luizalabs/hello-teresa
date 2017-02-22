import falcon


class Hello:
    def on_get(self, req, resp):
        resp.body = 'Hello World!'


api = falcon.API()
api.add_route('/', Hello())
