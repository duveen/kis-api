import json


class IllegalArgumentError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class APIServerError(RuntimeError):
    def __init__(self, response):
        reason = json.loads(response.text)
        reason = f"[{response.status_code}] {reason['error_code']}: {reason['error_description']}"
        super().__init__(reason)
