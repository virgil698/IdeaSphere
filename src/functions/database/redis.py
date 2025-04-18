import redis

class RedisManager:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def get_connection(self, db_number):
        return redis.StrictRedis(
            host=self.host,
            port=self.port,
            db=db_number,
            password=self.password,
            decode_responses=True
        )

    def get_fans_db(self):
        return self.get_connection(0)

    def get_following_db(self):
        return self.get_connection(1)

    def get_contributions_db(self):
        return self.get_connection(3)
