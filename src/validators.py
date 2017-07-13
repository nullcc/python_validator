# -*- coding: utf-8 -*-

import re

__author__ = "nullcc"


class ValidationError(ValueError):

    def __init__(self, message="", *args, **kwargs):
        self.message = message
        ValueError.__init__(self, message, *args, **kwargs)


class RequestValidator(ValueError):

    def __init__(self, request, field, pre_validators, pre_handlers, validators):
        self.request = request
        self.field = field
        self.pre_validators = pre_validators
        self.pre_handlers = pre_handlers
        self.validators = validators

    def __call__(self):
        for pre_validator in self.pre_validators:
            pre_validator(self.request, self.field)

        value = self.request.get(self.field)

        for pre_handler in self.pre_handlers:
            value = pre_handler(value)

        for validator in self.validators:
            validator(self.field, value)

        return value


class DataRequired(object):

    """
        验证字段存在性
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, data, field):
        if not data.get(field):
            message = self.message
            if message is None:
                message = "{} is required".format(field)
            raise ValidationError(message)


class EqualTo(object):

    """
        验证字段相等
    """

    def __init__(self, value, message=None):
        self.value = value
        self.message = message

    def __call__(self, field, req_value):
        if req_value == self.value:
            return
        message = self.message
        raise ValidationError(message)


class GreaterThan(object):

    """
        验证字段大于某个值
    """

    def __init__(self, value, message=None):
        self.value = value
        self.message = message

    def __call__(self, field, req_value):
        if req_value > self.value:
            return
        message = self.message
        if message is None:
            message = "{} must be greater than {}".format(field, self.value)
        raise ValidationError(message)


class GreaterThanOrEqualTo(object):

    """
        验证字段大于等于某个值
    """

    def __init__(self, value, message=None):
        self.value = value
        self.message = message

    def __call__(self, field, req_value):
        if req_value >= self.value:
            return
        message = self.message
        if message is None:
            message = "{} must be greater than or equal to {}".format(field, self.value)
        raise ValidationError(message)


class LessThan(object):

    """
        验证字段小于某个值
    """

    def __init__(self, value, message=None):
        self.value = value
        self.message = message

    def __call__(self, field, req_value):
        if req_value < self.value:
            return
        message = self.message
        if message is None:
            message = "{} must be less than {}".format(field, self.value)
        raise ValidationError(message)


class LessThanOrEqualTo(object):

    """
        验证字段小于等于某个值
    """

    def __init__(self, value, message=None):
        self.value = value
        self.message = message

    def __call__(self, field, req_value):
        if req_value <= self.value:
            return
        message = self.message
        if message is None:
            message = "{} must be less than or equal to {}".format(field, self.value)
        raise ValidationError(message)


class Regexp(object):

    """
        验证字段匹配正则表达式
    """

    def __init__(self, regex, flags=0, message=None):
        self.regex = re.compile(regex, flags)
        self.message = message

    def __call__(self, field, req_data, message=None):
        match = self.regex.match(req_data)
        if not match:
            if message is None:
                message = "{} is not match to {}".format(field, self.regex)
            raise ValidationError(message)
        return match


class Email(Regexp):

    """
        验证字段匹配电子邮件地址
    """

    def __init__(self, message=None):
        pattern = r"^.+@([^.@][^@]+)$"
        super(Email, self).__init__(pattern, re.IGNORECASE, message)

    def __call__(self, field, req_data, message=None):
        message = self.message
        if message is None:
            message = "Invalid email address."
        match = super(Email, self).__call__(field, req_data, message)
        if not match:
            raise ValidationError(message)


class MacAddress(Regexp):

    """
        验证字段匹配mac地址
    """

    def __init__(self, message=None):
        pattern = r"^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"
        super(MacAddress, self).__init__(pattern, re.IGNORECASE, message)

    def __call__(self, field, req_data, message=None):
        message = self.message
        if message is None:
            message = "Invalid mac address."
        match = super(MacAddress, self).__call__(field, req_data, message)
        if not match:
            raise ValidationError(message)


class URL(Regexp):

    """
        验证字段匹配URL
    """

    def __init__(self, message=None):
        pattern = r"^[a-z]+://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?$"
        super(URL, self).__init__(pattern, re.IGNORECASE, message)

    def __call__(self, field, req_data, message=None):
        message = self.message
        if message is None:
            message = "Invalid url."
        match = super(URL, self).__call__(field, req_data, message)
        if not match:
            raise ValidationError(message)


class UUID(Regexp):

    """
        验证字段匹配UUID
    """

    def __init__(self, message=None):
        pattern = r"^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$"
        super(UUID, self).__init__(pattern, re.IGNORECASE, message)

    def __call__(self, field, req_data, message=None):
        message = self.message
        if message is None:
            message = "Invalid uuid."
        match = super(UUID, self).__call__(field, req_data, message)
        if not match:
            raise ValidationError(message)


class Length(object):

    """
        验证字段长度
    """

    def __init__(self, min_length=-1, max_length=-1, message=None):
        self.min_length = min_length
        self.max_length = max_length
        self.message = message

    def __call__(self, field, req_data, message=None):
        if self.min_length != -1:
            # 设置了最小长度
            if len(req_data) < self.min_length:
                message = "length of {} should not be less than {}".format(field, self.min_length)
                raise ValidationError(message)

        if self.max_length != -1:
            # 设置了最大长度
            if len(req_data) > self.max_length:
                message = "length of {} should not be greater than {}".format(field, self.max_length)
                raise ValidationError(message)


class NumberRange(object):

    """
        验证字段数字范围
    """

    def __init__(self, min_num=None, max_num=None, message=None):
        self.min_num = min_num
        self.max_num = max_num
        self.message = message

    def __call__(self, field, req_data, message=None):
        if self.min_num is not None:
            # 设置了最小值
            if req_data < self.min_num:
                message = "{} should not be less than {}".format(field, self.min_num)
                raise ValidationError(message)

        if self.max_num is not None:
            # 设置了最大值
            if req_data > self.max_num:
                message = "{} should not be greater than {}".format(field, self.max_num)
                raise ValidationError(message)
