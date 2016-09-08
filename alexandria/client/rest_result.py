class RestResult:
    def __init__(self, uuid=None, json=None, failed=False, response=None):
        self.uuid = uuid
        self.json = json
        self.failed = failed
        self.response = response

    def __str__(self):
        return "<RestResult failed={}, uuid={}, json={}, response={}>" \
            .format(self.failed, self.uuid, self.json, self.response)
