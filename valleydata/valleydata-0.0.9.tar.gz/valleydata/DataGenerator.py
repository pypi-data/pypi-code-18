from faker import Factory


class DataGenerator:
    def __init__(self):
        self.fake = Factory.create()

    def personal_data(self, amount=1):
        result = []
        for _ in range(amount):
            result.append({
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'address': self.fake.address(),
                'birthday': self.fake.date_time(tzinfo=None)
            })
        return result

    def geo_data(self, amount=1):
        result = []
        for _ in range(amount):
            result.append({
                'city': self.fake.city(),
                'country': self.fake.country_code(),
                'latitude': self.fake.latitude(),
                'longitude': self.fake.longitude()
            })
        return result