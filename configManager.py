import json
import os
from datetime import date

DEFAULT_DAILY_GOAL = 2000
DEFAULT_SIP_AMOUNT = 250
PATH_CONFIG = "config.json"
DEFAULT_CONFIG = {
    "dailyGoal": DEFAULT_DAILY_GOAL,
    "sipAmount": DEFAULT_SIP_AMOUNT,
    "currentIntake": 0,
    "lastResetDate": None,
    "streak": 0
}

class ConfigManager:
    def __init__(self):
        self.data = DEFAULT_CONFIG.copy()
        self.load()
        self.resetOnNewDay()

    @property
    def dailyGoal(self) -> int:
        return self.data["dailyGoal"]

    @dailyGoal.setter
    def dailyGoal(self, value: int):
        self.data["dailyGoal"] = value
        self.save()

    @property
    def sipAmount(self) -> int:
        return self.data["sipAmount"]

    @sipAmount.setter
    def sipAmount(self, value: int):
        self.data["sipAmount"] = value
        self.save()

    @property
    def currentIntake(self) -> int:
        return self.data["currentIntake"]

    def addIntake(self, amount: int):
        self.data["currentIntake"] += amount
        self.save()

    @property
    def streak(self) -> int:
        return self.data["streak"]

    def resetOnNewDay(self):
        currDate = date.today().isoformat()
        lastReset = self.data["lastResetDate"]

        # If date not recorded yet, initialise it first
        if lastReset is None:
            self.data["lastResetDate"] = currDate
            self.save()
            lastReset = currDate

        if lastReset != currDate:
            if self.data["currentIntake"] >= self.data["dailyGoal"]:
                self.data["streak"] += 1
            else:
                self.data["streak"] = 0
            self.data["currentIntake"] = 0
            self.data["lastResetDate"] = currDate
            self.save()

    def load(self):
        if os.path.exists(PATH_CONFIG):
            try:
                with open(PATH_CONFIG, "r") as fp:
                    data = json.load(fp)
                self.data.update(data)
            except (json.JSONDecodeError, OSError):
                self.data = DEFAULT_CONFIG.copy()
                self.save()
        else:
            self.save()

    def save(self):
        try:
            with open(PATH_CONFIG, "w") as fp:
                json.dump(self.data, fp)
        except OSError:
            pass
