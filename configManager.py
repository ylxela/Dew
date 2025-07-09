import json
import os
from datetime import date
import time


DEFAULT_DAILY_GOAL = 2000
DEFAULT_SIP_AMOUNT = 250
PATH_CONFIG = "config.json"
DEFAULT_CONFIG = {
    "dailyGoal": DEFAULT_DAILY_GOAL,
    "sipAmount": DEFAULT_SIP_AMOUNT,
    "currentIntake": 0,
    "lastResetDate": None,
    "streak": 0,
    "lastIntakeTime": 0
}

class ConfigManager:
    """Manages application configuration & daily water intake tracking."""

    def __init__(self):
        self.data = DEFAULT_CONFIG.copy()
        self.load()
        self.resetOnNewDay()

    @property
    def dailyGoal(self) -> int:
        """Get daily water intake goal in mL"""
        return self.data["dailyGoal"]

    @dailyGoal.setter
    def dailyGoal(self, value: int):
        """Set daily water intake goal in mL"""
        self.data["dailyGoal"] = value
        self.save()

    @property
    def sipAmount(self) -> int:
        """Get sip amount in mL"""
        return self.data["sipAmount"]

    @sipAmount.setter
    def sipAmount(self, value: int):
        """Set sip amount in mL"""
        self.data["sipAmount"] = value
        self.save()

    @property
    def lastIntakeTime(self) -> float:
        return self.data.get("lastIntakeTime", 0)

    @lastIntakeTime.setter
    def lastIntakeTime(self, value: float):
        """Set the timestamp of last intake."""
        self.data["lastIntakeTime"] = value
        self.save()

    @property
    def currentIntake(self) -> int:
        """Get current daily intake in mL"""
        return self.data["currentIntake"]

    def addIntake(self, amount: int):
        """Add water intake amount and save configuration."""
        self.data["currentIntake"] += amount
        self.data["lastIntakeTime"] = time.time()
        self.save()

    @property
    def streak(self) -> int:
        """Get current streak of consecutive days meeting goal."""
        return self.data["streak"]

    def resetOnNewDay(self):
        """Reset daily intake and update streak on new day."""
        currentDate = date.today().isoformat()
        lastResetDate = self.data["lastResetDate"]

        if lastResetDate is not None and lastResetDate != currentDate:
            if self.data["currentIntake"] >= self.data["dailyGoal"]:
                self.data["streak"] += 1
            else:
                self.data["streak"] = 0
            self.data["currentIntake"] = 0
            self.data["lastResetDate"] = currentDate
            self.save()

    def load(self):
        """Load configuration from file."""
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
        """Save configuration to file."""
        try:
            with open(PATH_CONFIG, "w") as fp:
                json.dump(self.data, fp)
        except OSError:
            pass
