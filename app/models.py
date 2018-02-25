from app import db

class User(db.Model):
    id = db.Column(db.String(128), primary_key = True)
    nickname = db.Column(db.String(128), index = True, unique = True)
    gender = db.Column(db.String(128), index = True, unique = True)
    country = db.Column(db.String(128), index = True, unique = True)
    province = db.Column(db.String(128), index = True, unique = True)
    city = db.Column(db.String(128), index = True, unique = True)
    created_time = db.Column(db.DateTime)
    updated_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<User id %r, User name %r>' % (self.id, self.nickname)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(128), index = True)
    consignee_address = db.Column(db.String(1024), index = True)
    consignee_phone = db.Column(db.String(64), index = True)
    consignee_name = db.Column(db.String(128), index = True)

    def __repr__(self):
        return '<Address %r, User id %r>' %(self.consignee_address, self.openid)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

class UserWX(db.Model):
    id = db.Column(db.String(1024), primary_key = True)
    openid = db.Column(db.String(128), index = True)
    session_key = db.Column(db.String(1024), index = True)
    created_time = db.Column(db.DateTime)
    updated_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<UserWX id %r>' %(self.id)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
