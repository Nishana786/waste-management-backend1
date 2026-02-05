from datetime import datetime
from app.extensions import db
from app.models.driver import Driver


def approve_item(item):
    if item.status != "pending":
        raise ValueError("Invalid state change")

    item.status = "approved"
    item.updated_at = datetime.utcnow()
    db.session.commit()


def reject_item(item):
    item.status = "rejected"
    item.updated_at = datetime.utcnow()
    item.notification_sent = False   # 🔔 VERY IMPORTANT
    db.session.commit()


def complete_item(item):
    item.status = "completed"
    item.updated_at = datetime.utcnow()
    item.notification_sent = False  

    if item.driver:
        item.driver.status = "available"

    db.session.commit()


def assign_driver(task, driver_id):
    driver = Driver.query.get_or_404(driver_id)

    if task.status != "approved":
        raise ValueError("Task not approved yet")

    task.driver_id = driver.id
    task.status = "assigned"
    task.updated_at = datetime.utcnow()

    driver.status = "assigned"
    db.session.commit()
