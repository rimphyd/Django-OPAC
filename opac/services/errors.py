class ServiceError(Exception):
    pass


class LendingAlreadyExistsError(ServiceError):
    pass


class RenewingAlreadyExistsError(ServiceError):
    pass


class ReservationExistsError(ServiceError):
    pass
