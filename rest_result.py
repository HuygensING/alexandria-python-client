class RestResult:
    def __init__(self, cargo=None, failed=False, response=None):
        self.cargo = cargo
        self.failed = failed
        self.response = response
