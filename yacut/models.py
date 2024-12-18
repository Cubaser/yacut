import random
import re
from datetime import datetime

from flask import url_for

from yacut import db
from .error_handlers import InvalidAPIUsage
from settings import (API_MESSAGE_BAD_CUSTOM_ID,
                      API_MESSAGE_DOUBLE_CUSTOM_ID,
                      CHARS,
                      CUSTOM_ID_MAX_LEN,
                      CUSTOM_ID_PATTERN,
                      MAX_RETRIES,
                      SHORT_LINK_LENGTH)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    @classmethod
    def validate_short_id(cls, short_id):
        if (not re.fullmatch(CUSTOM_ID_PATTERN, short_id) or
                len(short_id) > CUSTOM_ID_MAX_LEN):
            return True
        return False

    @classmethod
    def get_unique_short_id(cls):
        for _ in range(MAX_RETRIES):
            short_id = ''.join(random.choices(CHARS, k=SHORT_LINK_LENGTH))
            if not cls.check_unique_short_id(short_id):
                return short_id
        return cls.get_url_by_short_id()

    @classmethod
    def check_unique_short_id(cls, short_id):
        return cls.get_url_by_short_id(short_id).first() is not None

    @classmethod
    def get_url_by_short_id(cls, short_id):
        return cls.query.filter_by(short=short_id)

    @classmethod
    def create_short_link(cls, original, custom_id):
        if not custom_id:
            custom_id = cls.get_unique_short_id()
        if cls.validate_short_id(custom_id):
            raise InvalidAPIUsage(API_MESSAGE_BAD_CUSTOM_ID)
        if cls.check_unique_short_id(custom_id):
            raise InvalidAPIUsage(API_MESSAGE_DOUBLE_CUSTOM_ID)
        url_map = cls(original=original, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map
