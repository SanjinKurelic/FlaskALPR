from app import database


class LicencePlate(database.db.Model):
    plate = database.db.Column(database.db.String(8), primary_key=True)
    time = database.db.Column(database.db.BigInteger, primary_key=True)

    def save(self):
        database.db.session.add(self)
        database.db.session.commit()
