

class HTMXMiddleware:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        headers = request.headers
        response = self._get_response(request)
        return response
