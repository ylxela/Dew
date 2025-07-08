import json
import os
from datetime import date

DEFAULT_DAILY_GOAL = 2000
DEFAULT_SIP_AMOUNT = 250

class ConfigManager:
    DEFAULTS = {
        "dailyGoal": DEFAULT_DAILY_GOAL,
        "sipAmount": DEFAULT_SIP_AMOUNT,
        "currentIntake": 0,
        "lastResetDate": None,
        "streak": 0
    }

    def __init__(self, path: str = "config.json") -> None:
        self.path = os.path.join(os.path.dirname(__file__), path)
        self.data = self.DEFAULTS.copy()
        self.load()
        self.resetOnNewDay()

    @property
    def dailyGoal(self) -> int:
        return self.data["dailyGoal"]

    @dailyGoal.setter
    def dailyGoal(self, value: int):
        self.data["dailyGoal"] = int(value)
        self.save()

    @property
    def sipAmount(self) -> int:
        return self.data["sipAmount"]

    @sipAmount.setter
    def sipAmount(self, value: int):
        self.data["sipAmount"] = int(value)
        self.save()

    @property
    def currentIntake(self) -> int:
        return self.data["currentIntake"]

    @property
    def streak(self) -> int:
        return self.data["streak"]

    def addIntake(self, amount: int):
        """Add water intake and save config."""
        self.data["currentIntake"] += amount

        self.data["currentIntake"] = min(self.data["currentIntake"], self.data["dailyGoal"] * 2)
        self.save()

    def resetOnNewDay(self):
        todayStr = date.today().isoformat()
        lastReset = self.data.get("lastResetDate")
        if lastReset != todayStr:

            if lastReset is not None and self.data.get("currentIntake", 0) >= self.data["dailyGoal"]:
                self.data["streak"] += 1
            else:

                if lastReset is not None:
                    self.data["streak"] = 0


            self.data["currentIntake"] = 0
            self.data["lastResetDate"] = todayStr
            self.save()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as fp:
                    loaded = json.load(fp)

                self.data.update(loaded)
            except (json.JSONDecodeError, OSError):

                self.data = self.DEFAULTS.copy()
                self.save()
        else:
            self.save()

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as fp:
                json.dump(self.data, fp, indent=2)
        except OSError:
            pass
