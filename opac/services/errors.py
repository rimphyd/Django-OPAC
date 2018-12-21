class ServiceError(Exception):
    pass


class LendingAlreadyExistsError(ServiceError):
    pass
