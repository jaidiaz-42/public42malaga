import json
from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError("Mission ID must start with 'M'")

        has_leadership = any(
            c.rank in (Rank.COMMANDER, Rank.CAPTAIN) for c in self.crew
        )
        if not has_leadership:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced_count = sum(1 for c in self.crew if
                                    c.years_experience >= 5)
            if experienced_count < (len(self.crew) / 2):
                raise ValueError(
                    "Long missions (> 365 days) need "
                    "50% experienced crew (5+ years)"
                )

        if not all(c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    try:
        with open("generated_data/space_missions.json", "r") as f:
            missions_data = json.load(f)
    except FileNotFoundError:
        return

    print("Space Mission Crew Validation")
    print("=========================================")

    for i, data in enumerate(missions_data):
        try:
            mission = SpaceMission(**data)
            print("Valid mission created:")
            print(f"Mission: {mission.mission_name}")
            print(f"ID: {mission.mission_id}")
            print(f"Destination: {mission.destination}")
            print(f"Duration: {mission.duration_days} days")
            print(f"Budget: ${mission.budget_millions}M")
            print(f"Crew size: {len(mission.crew)}")
            print("Crew members:")
            for member in mission.crew:
                print(f"- {member.name} ({member.rank.value}) - "
                      f"{member.specialization}")
        except ValidationError as e:
            print("Expected validation error:")
            for error in e.errors():
                msg = error.get("msg", "")
                if msg.startswith("Value error, "):
                    msg = msg.replace("Value error, ", "")
                print(msg)

        if i < len(missions_data) - 1:
            print("\n=========================================")


if __name__ == "__main__":
    main()
