from app.models.driver import Driver
from app.extensions import db

class DriverRepository:

    @staticmethod
    def create(data):
        driver = Driver(**data)
        db.session.add(driver)
        db.session.commit()
        return driver

    @staticmethod
    def get_all():
        return Driver.query.all()

    @staticmethod
    def delete(driver_id):
        driver = Driver.query.get_or_404(driver_id)

        if driver.reports or driver.pickups:
           raise ValueError("Driver has assigned tasks")

        db.session.delete(driver)
        db.session.commit()
    

    @staticmethod
    def mark_completed(driver_id):
        driver = Driver.query.get_or_404(driver_id)
        driver.status = "completed"
        db.session.commit()
        return driver

    @staticmethod
    def mark_assigned(driver_id):
        driver = Driver.query.get(driver_id)
        if not driver:
            raise ValueError("Driver not found")

        driver.status = "assigned"
        db.session.commit()
        return driver

