class Singleton(type):
    _instances = {}
    _extra_msg = None

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # _instances is empty or cls is not registered yet... initialize it and create an entry
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # For silent operation, set _printout to False
        # elif kwargs.pop('_printout', True):
        #     logger.debug("Base -> __call__ -> {}: Module is already instantiated...".format(cls.__name__))
        #     if cls._extra_msg:
        #         logger.debug("Base -> __call__ -> {}: {}".format(cls.__name__, cls._extra_msg))
        return cls._instances[cls]

