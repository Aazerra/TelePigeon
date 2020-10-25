import abc


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
