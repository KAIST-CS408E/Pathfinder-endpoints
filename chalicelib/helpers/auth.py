import hashlib
import hmac
import datetime
from uuid import uuid4

import jwt
from chalice import UnauthorizedError
from chalicelib.helpers.credential import AUTH_SECRET

_SECRET = AUTH_SECRET


def get_jwt_token(username, password, record):
    actual = hashlib.pbkdf2_hmac(
        record['hash'],
        bytearray(password, encoding='utf-8'),
        record['salt'].value,
        record['rounds']
    )
    expected = record['hashed'].value
    if hmac.compare_digest(actual, expected):
        now = datetime.datetime.utcnow()
        unique_id = str(uuid4())
        payload = {
            'sub': username,
            'iat': now,
            'nbf': now,
            'jti': unique_id,
            # NOTE: We can also add 'exp' if we want tokens to expire.
        }
        return jwt.encode(payload, _SECRET, algorithm='HS256').decode('utf-8')
    raise UnauthorizedError('Invalid password')


def decode_jwt_token(token):
    return jwt.decode(token, _SECRET, algorithms=['HS256'])