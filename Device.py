from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Any, Dict
from enum import Enum

class LevelStatus(str, Enum):
    normal = "normal"
    low = "low"
    high = "high"

class DeviceStatus(str, Enum):
    online = "online"
    offline = "offline"
    warning = "warning"

@dataclass
class SmokeSensor:
    value: float = 0.0
    unit: str = "ppm"
    status: LevelStatus = LevelStatus.normal

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SmokeSensor":
        return SmokeSensor(
            value=float(d.get("value", 0)),
            unit=d.get("unit", "ppm"),
            status=LevelStatus(d.get("status", "normal"))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "unit": self.unit, "status": self.status.value}

@dataclass
class TemperatureSensor:
    value: float = 0.0
    unit: str = "C"
    status: LevelStatus = LevelStatus.normal

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TemperatureSensor":
        return TemperatureSensor(
            value=float(d.get("value", 0)),
            unit=d.get("unit", "C"),
            status=LevelStatus(d.get("status", "normal"))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "unit": self.unit, "status": self.status.value}

@dataclass
class FlameSensor:
    detected: bool = False
    sensitivity: float = 0.0

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FlameSensor":
        return FlameSensor(
            detected=bool(d.get("detected", False)),
            sensitivity=float(d.get("sensitivity", 0))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"detected": self.detected, "sensitivity": self.sensitivity}

@dataclass
class SensorData:
    smoke: SmokeSensor = field(default_factory=SmokeSensor)
    temperature: TemperatureSensor = field(default_factory=TemperatureSensor)
    flame: FlameSensor = field(default_factory=FlameSensor)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SensorData":
        return SensorData(
            smoke=SmokeSensor.from_dict(d.get("smoke", {})),
            temperature=TemperatureSensor.from_dict(d.get("temperature", {})),
            flame=FlameSensor.from_dict(d.get("flame", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "smoke": self.smoke.to_dict(),
            "temperature": self.temperature.to_dict(),
            "flame": self.flame.to_dict(),
        }

@dataclass
class Alerts:
    count: int = 0
    latest: Optional[str] = None

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Alerts":
        return Alerts(count=int(d.get("count", 0)), latest=d.get("latest"))

    def to_dict(self) -> Dict[str, Any]:
        return {"count": self.count, **({"latest": self.latest} if self.latest is not None else {})}

@dataclass
class Device:
    id: str = ""
    user_id: str = ""
    device_id: str = ""
    name: Optional[str] = ""
    status: Optional[DeviceStatus] = DeviceStatus.offline
    last_update: Optional[str] = ""
    sensors: Optional[SensorData] = field(default_factory=SensorData)
    alerts: Optional[Alerts] = field(default_factory=Alerts)
    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Device":
        return Device(
            id=str(d.get("id", "")),
            device_id=str(d.get("device_id", "")),
            user_id=str(d.get("user_id", "")),
            name=str(d.get("name", "")),
            status=DeviceStatus(d.get("status", "offline")),
            last_update=str(d.get("lastUpdate", "")),
            sensors=SensorData.from_dict(d.get("sensors", {})),
            alerts=Alerts.from_dict(d.get("alerts", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "device_id": self.device_id,
            "user_id": self.user_id,
            "name": self.name,
            "status": self.status.value,
            "lastUpdate": self.last_update,
            "sensors": self.sensors.to_dict(),
            "alerts": self.alerts.to_dict(),
        }
