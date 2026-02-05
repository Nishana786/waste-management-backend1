from app.repository.driver_repository import DriverRepository


class DriverRouteHandler:

    @staticmethod
    def add_driver(data):
        return DriverRepository.create(data)

    @staticmethod
    def get_drivers():
        return DriverRepository.get_all()

    @staticmethod
    def delete_driver(driver_id):
        DriverRepository.delete(driver_id)

    @staticmethod
    def complete_driver(driver_id):
        DriverRepository.mark_completed(driver_id)

    @staticmethod
    def assign_driver(driver_id):
        DriverRepository.assign(driver_id)
