import time

class RequestTimerMiddleware:
    def __init__(self, get_response):
        print("Server running, RequestTimerMiddleware init")
        self.get_response = get_response

    def __call__(self, request):
        print("Call going:", request.path)
        response = self.get_response(request)
        print("Response going:", response.status_code)
        return response

class TimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        response["X-Process-Time"] = str(duration)
        print(f"[TIMER] {request.path} processed in {duration:.4f} sec")
        return response