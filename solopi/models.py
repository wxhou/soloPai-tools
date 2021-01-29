from .extensions import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(512))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    solopifiles = db.relationship('SoloPiFile', back_populates='product')

    def __repr__(self):
        return self.name


class SoloPiTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cn_name = db.Column(db.String(128))
    en_name = db.Column(db.String(128))
    csv_title = db.Column(db.String(128))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return self.cn_name


class SoloPiFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))
    filepath = db.Column(db.String(512))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='solopifiles')

    def __repr__(self):
        return self.filename
