class PyPokedexError(RuntimeError):
    pass


class PyPokedexHTTPError(PyPokedexError):
    def __init__(self, message: str, http_code: int) -> None:
        super().__init__(message)
        self._http_code = http_code

    @property
    def http_code(self) -> int:
        return self._http_code
