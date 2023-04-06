class NoResultFound(Exception):
    "Raised when the input value is not found in the cache data"
    def __init__(self, ) -> None:
        self.msg = "No result found. Wrong id"

        print(self.msg)
