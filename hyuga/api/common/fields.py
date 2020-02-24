from cerberus import SchemaError, Validator

from hyuga.core.errors import InvalidParameterError
from hyuga.core.log import _api_logger

FIELDS = {
    "username": {
        "type": "string",
        "regex": r"^[0-9a-zA-Z_]{4,30}$",
        "required": True
    },
    "nickname": {
        "type": "string"
    },
    "password": {
        "type": "string",
        "required": True,
        "minlength": 8,
        "maxlength": 64
    },
    "recordType": {
        "type": "string",
        "regex": r"(dns|http)",
        "required": True,
    },
    "userToken": {
        "type": "string",
        "regex": r"[A-Za-z0-9]{22,32}",
        "required": True,
    },
    "recordsFilter": {
        "type": "string",
        "regex": r"[A-Za-z0-9-]{1,20}",
        "maxlength": 20
    }

}


class BaseValidate:
    """BaseValidate 根据 schema 对数据进行验证
    """

    def __init__(self, schema, is_params=False):
        self.schema = schema
        self.is_params = is_params

    def validate(self, req, resp, resource, params):
        v = Validator(self.schema)
        if self.is_params:
            doc = req.params
        else:
            doc = req.context.get("data", None)
        _api_logger.debug(doc)
        try:
            if doc:
                if isinstance(doc, dict):
                    if not v.validate(doc):
                        raise InvalidParameterError(v.errors)
                else:
                    raise InvalidParameterError(
                        "Invalid doc %s .it must be a dict" % doc)
            else:
                raise InvalidParameterError("Invalid Request %s" % doc)
        except SchemaError:
            raise InvalidParameterError("Invalid Request %s" % doc)
