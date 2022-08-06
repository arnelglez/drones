from apscheduler.schedulers.background import BackgroundScheduler
from api.views import DroneBatteryLogList


def start():
    scheduler = BackgroundScheduler()
    log = DroneBatteryLogList()
    scheduler.add_job(log.save_drone_batery_log, "interval", minutes=60, id="log_001", replace_existing=True)
    scheduler.start()