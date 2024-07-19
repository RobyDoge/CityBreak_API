from enum import Enum


class ReturnCode(Enum):
      OK = 200
      CREATED = 201
      NO_CONTENT = 204
      BAD_REQUEST = 400
      NOT_FOUND = 404