# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('.')
import unittest
from src.handlers import to_int, to_float, to_str
from src.validators import (RequestValidator, EqualTo,
                            GreaterThan, DataRequired,
                            LessThan, Regexp, Email,
                            MacAddress, URL, UUID, Length,
                            NumberRange)

data = dict(num=42,
            text="abc",
            email="nullcc@gmail.com",
            mac="80:80:fe:1a:08:13",
            url="http://www.google.com",
            uuid="550E8400-E29B-11D4-A716-446655440000",
            name="nullcc",
            age=28)


num = RequestValidator(data,
                       "num",
                       pre_validators=[DataRequired()],
                       pre_handlers=[to_int],
                       validators=[
                           GreaterThan(10)
                       ])()

text = RequestValidator(data,
                        "text",
                        pre_validators=[DataRequired("text is required")],
                        pre_handlers=[to_str],
                        validators=[
                            EqualTo("abc", "text must be equal to abc")
                        ])()

email = RequestValidator(data,
                         "email",
                         pre_validators=[DataRequired("email is required")],
                         pre_handlers=[to_str],
                         validators=[
                             Email()
                         ])()

mac = RequestValidator(data,
                       "mac",
                       pre_validators=[DataRequired("mac addresz is required")],
                       pre_handlers=[to_str],
                       validators=[
                           MacAddress()
                       ])()

url = RequestValidator(data,
                       "url",
                       pre_validators=[DataRequired("url is required")],
                       pre_handlers=[to_str],
                       validators=[
                           URL()
                       ])()

uuid = RequestValidator(data,
                        "uuid",
                        pre_validators=[DataRequired("uuid is required")],
                        pre_handlers=[to_str],
                        validators=[
                            UUID()
                        ])()

name = RequestValidator(data,
                        "name",
                        pre_validators=[DataRequired("name is required")],
                        pre_handlers=[to_str],
                        validators=[
                            Length(min_length=6, max_length=10)
                        ])()

age = RequestValidator(data,
                       "age",
                       pre_validators=[DataRequired("age is required")],
                       pre_handlers=[to_int],
                       validators=[
                           NumberRange(min_num=1, max_num=99)
                       ])()

data = dict(num=42,
            text="abc",
            email="nullcc@gmail.com",
            mac="80:80:fe:1a:08:13",
            url="http://www.google.com",
            uuid="550E8400-E29B-11D4-A716-446655440000",
            name="nullcc",
            age=28)

assert num == 42
assert text == "abc"
assert email == "nullcc@gmail.com"
assert mac == "80:80:fe:1a:08:13"
assert url == "http://www.google.com"
assert uuid == "550E8400-E29B-11D4-A716-446655440000"
assert name == "nullcc"
assert age == 28

print("test done.")

if __name__ == '__main__':
    unittest.main()
