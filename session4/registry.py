# registry.py

class_registry = {}

class AutoRegister(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "BaseService":
            class_registry[name] = cls
            print(f"[AutoRegister] Registered {name}")
        return cls

# Example usage
if __name__ == "__main__":
    class BaseService(metaclass=AutoRegister):
        pass

    class UserService(BaseService):
        pass

    class OrderService(BaseService):
        pass

    print(class_registry)  # {'UserService': ..., 'OrderService': ...}
