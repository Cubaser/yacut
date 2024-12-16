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

    def save_api_data(self):
        if self.short is None:
            self.short = self.get_unique_short_id()
        if self.validate_short_id(self.short):
            raise InvalidAPIUsage(API_MESSAGE_BAD_CUSTOM_ID)
        if self.check_unique_short_id(self.short):
            raise InvalidAPIUsage(API_MESSAGE_DOUBLE_CUSTOM_ID)
        url = URLMap(
            original=self.original,
            short=self.short
        )
        db.session.add(url)
        db.session.commit()

    def save_data(self):
        if self.short is None:
            self.short = self.get_unique_short_id()
        url = URLMap(
            original=self.original,
            short=self.short
        )
        db.session.add(url)
        db.session.commit()

    def validate_short_id(self, short_id):
        if (not re.fullmatch(CUSTOM_ID_PATTERN, short_id) or
                len(short_id) > CUSTOM_ID_MAX_LEN):
            return True
        return False

    def get_unique_short_id(self):
        for _ in range(MAX_RETRIES):
            short_id = ''.join(random.choices(CHARS, k=SHORT_LINK_LENGTH))
            if not URLMap.check_unique_short_id(short_id):
                return short_id
        return self.get_url_by_short_id()

    @classmethod
    def check_unique_short_id(cls, short_id):
        if URLMap.get_url_by_short_id(short_id).first() is not None:
            return True
        return False

    @classmethod
    def get_url_by_short_id(cls, short_id):
        return cls.query.filter_by(short=short_id)
