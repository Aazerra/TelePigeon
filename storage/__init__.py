import abc


# class StorageMeta(type):
#     def __new__(cls, name, bases, body):
#         if name != 'StorageMeta' and not 'bar' in body:
#             raise TypeError("bad user class")
#         print('BaseMeta.__new__', cls, name, bases, body)
#         return super().__new__(cls, name, bases, body)
#

class Storage(abc.ABC):
    @abc.abstractmethod
    def get_user(self, user_id):
        pass

    @abc.abstractmethod
    def register_user(self, user_id: int, user_data):
        pass

    @abc.abstractmethod
    def get_admin(self):
        pass

    @abc.abstractmethod
    def save_message_id(self, message_id, user_id):
        pass

    @abc.abstractmethod
    def get_message_info(self, message_id):
        pass
