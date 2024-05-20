class NodeNameError(Exception):
    def init(self, message, extra_info):
        super().init(message)
        self.extra_info = extra_info