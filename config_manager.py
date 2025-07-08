import json
import os
from datetime import datetime, date


class ConfigManager:
    """Handle persistent configuration and daily hydration data."""

    DEFAULTS = {
        "daily_goal": 2000,
        "sip_amount": 250,
        "current_intake": 0,
        "last_reset_date": None,
        "streak": 0
    }

    def __init__(self, path: str = "config.json") -> None:
        self.path = os.path.join(os.path.dirname(__file__), path)
        self.data = self.DEFAULTS.copy()
        self._load()
        self._reset_if_new_day()

    # Properties for convenient access
    @property
    def daily_goal(self) -> int:
        return self.data["daily_goal"]

    @daily_goal.setter
    def daily_goal(self, value: int):
        self.data["daily_goal"] = int(value)
        self._save()

    @property
    def sip_amount(self) -> int:
        return self.data["sip_amount"]

    @sip_amount.setter
    def sip_amount(self, value: int):
        self.data["sip_amount"] = int(value)
        self._save()

    @property
    def current_intake(self) -> int:
        return self.data["current_intake"]

    @property
    def streak(self) -> int:
        return self.data["streak"]

    def add_intake(self, amount: int):
        """Add water intake and save config."""
        self.data["current_intake"] += amount
        
        self.data["current_intake"] = min(self.data["current_intake"], self.data["daily_goal"] * 2)
        self._save()

    def _reset_if_new_day(self):
        today_str = date.today().isoformat()
        last_reset = self.data.get("last_reset_date")
        if last_reset != today_str:
            
            if last_reset is not None and self.data.get("current_intake", 0) >= self.data["daily_goal"]:
                self.data["streak"] += 1
            else:
                
                if last_reset is not None:
                    self.data["streak"] = 0

            
            self.data["current_intake"] = 0
            self.data["last_reset_date"] = today_str
            self._save()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as fp:
                    loaded = json.load(fp)
                
                self.data.update(loaded)
            except (json.JSONDecodeError, OSError):
                
                self.data = self.DEFAULTS.copy()
                self._save()
        else:
            self._save()

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as fp:
                json.dump(self.data, fp, indent=2)
        except OSError:
            pass
