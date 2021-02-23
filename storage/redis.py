from models.user import User, AnonymousUser
from storage import Storage
from redis import ConnectionPool, Redis


class RedisStorage(Storage):
    def __init__(self, host="localhost", port=6379, db=0):
        self.pool = ConnectionPool(
            host=host, port=port, db=db, decode_responses=True)

    @property
    def _redis(self):
        return Redis(connection_pool=self.pool)

    def get_user(self, user_id):
        user_dict: dict = self._redis.hgetall(f"user:{user_id}")
        if not bool(user_dict):
            return AnonymousUser()
        return User(id=user_id, **user_dict)

    def get_admin(self):
        return int(self._redis.get("admin"))

    def set_admin(self, user_id):
        user_data = {
            "name": "None",
            "username": "None",
            "is_admin": "1"
        }
        with self._redis.pipeline() as pipe:
            for k, v in user_data.items():
                pipe.hset(f"user:{user_id}", k, v)
            pipe.execute()
        return self._redis.set("admin", user_id)

    def register_user(self, user_id: int, user_data):
        user_data = {
            "name": user_data.first_name,
            "username": user_data.username,
            "is_admin": "0"
        }
        with self._redis.pipeline() as pipe:
            for k, v in user_data.items():
                pipe.hset(f"user:{user_id}", k, v)
            pipe.execute()
        return User(id=user_id, **user_data)

    def save_message_id(self, message_id, user_id):
        self._redis.set(f"messages:{message_id}", user_id)

    def get_message_info(self, message_id):
        return int(self._redis.get(f"messages:{message_id}"))
