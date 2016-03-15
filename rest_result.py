class RestResult:
    def __init__(self, cargo=None, failed=False, response=None):
        self.cargo = cargo
        self.failed = failed
        self.response = response

    def __str__(self):
        return "<RestResult> failed={}, cargo={}, response={}".format(self.failed, self.cargo, self.response)
