class OverdraftException(Exception):
    def __init__(self, msg, deficit):
        super().__init__(msg)
        self.deficit = deficit

    def getDedicit(self):
        return self.deficit
