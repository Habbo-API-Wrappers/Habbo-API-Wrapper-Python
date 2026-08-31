from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Dict, List, TypedDict


class AbstractLevelUpper(ABC):

    def current_xp(self, xp: int) -> int:
        """Bound the value to within the allowed XP limits."""
        return min(max(xp, 0), self.max_xp())

    @abstractmethod
    def current_level(self, xp: int) -> int:
        """Get the current level for the given xp."""

    @abstractmethod
    def total_xp_required(self, xp: int) -> int:
        """Get the total amount of XP required to achieve the next level from the
        current level."""

    @abstractmethod
    def progress(self, xp: int) -> int:
        """Get the amount of XP past the current level."""

    @abstractmethod
    def progress_percentage(self, xp: int) -> int:
        """Get the percentage of progress to the next level."""

    @abstractmethod
    def xp_remaining(self, xp: int) -> int:
        """Get the amount of XP required to reach the next level."""

    @abstractmethod
    def is_maxed(self, xp: int) -> bool:
        """Return whether the variable has reached the max level or not."""

    @abstractmethod
    def max_level(self) -> int:
        """Get the maximum achievable level."""

    @abstractmethod
    def max_xp(self) -> int:
        """Get the maximum achievable XP."""


class LinearAbstractLevelUpper(AbstractLevelUpper):

    def __init__(self, step_size: int, maximum_level: int) -> None:
        self._step_size = step_size
        self._maximum_level = maximum_level

    def current_level(self, xp: int) -> int:
        return int(min(self._maximum_level, 1 + self.current_xp(xp) / self._step_size))

    def total_xp_required(self, xp: int) -> int:
        if self.is_maxed(xp):
            return 0
        return self._step_size

    def progress(self, xp: int) -> int:
        if self.is_maxed(xp):
            return 0
        return self.current_xp(xp) % self._step_size

    def progress_percentage(self, xp: int) -> int:
        if self.is_maxed(xp):
            return 0
        return int((self.progress(xp) / self._step_size) * 100)

    def xp_remaining(self, xp: int) -> int:
        if self.is_maxed(xp):
            return 0
        return self._step_size - (self.current_xp(xp) % self._step_size)

    def is_maxed(self, xp: int) -> bool:
        return self.current_level(xp) >= self._maximum_level

    def max_level(self) -> int:
        return self._maximum_level

    def max_xp(self) -> int:
        return self._maximum_level * self._step_size


class ExponentialAbstractLevelUpper(AbstractLevelUpper):

    def __init__(self, initial_xp: int, strength: int, maximum_level: int) -> None:
        self._initial_xp = initial_xp
        self._strength_as_decimal = strength / 100
        self._maximum_level = maximum_level
        self._max_xp_value = self._xp_for_level(maximum_level)

    def current_level(self, xp: int) -> int:
        current_xp = self.current_xp(xp)
        if current_xp <= 0:
            return 1

        log_base = 1 + self._strength_as_decimal
        level = int(
            math.log((current_xp * self._strength_as_decimal / self._initial_xp) + 1)
            / math.log(log_base)
        )

        if level > self._maximum_level:
            return self._maximum_level
        if level < 1:
            return 1
        if current_xp < self._xp_for_level(level):
            return max(level - 1, 1)
        if current_xp >= self._xp_for_level(level + 1):
            return min(self._maximum_level, level + 1)
        return level

    def total_xp_required(self, xp: int) -> int:
        if self.is_maxed(xp):
            return 0
        current_level = self.current_level(xp)
        return self._xp_for_level(current_level + 1) - self._xp_for_level(current_level)

    def progress(self, xp: int) -> int:
        current_xp = self.current_xp(xp)
        if self.is_maxed(current_xp):
            return 0
        current_level = self.current_level(xp)
        return current_xp - self._xp_for_level(current_level)

    def progress_percentage(self, xp: int) -> int:
        current_xp = self.current_xp(xp)
        if self.is_maxed(current_xp):
            return 0
        current_level = self.current_level(xp)
        level_xp = self._xp_for_level(current_level)
        next_level_xp = self._xp_for_level(current_level + 1)
        if level_xp == next_level_xp:
            return 100
        return int(((current_xp - level_xp) / (next_level_xp - level_xp)) * 100)

    def xp_remaining(self, xp: int) -> int:
        current_xp = self.current_xp(xp)
        if self.is_maxed(current_xp):
            return 0
        return self._xp_for_level(self.current_level(current_xp) + 1) - current_xp

    def is_maxed(self, xp: int) -> bool:
        return self.current_level(xp) >= self._maximum_level

    def max_level(self) -> int:
        return self._maximum_level

    def max_xp(self) -> int:
        return self._max_xp_value

    def _xp_for_level(self, level: int) -> int:
        if level < 1:
            return 0
        if level > self._maximum_level:
            return self._max_xp_value
        return int(
            self._initial_xp
            * (((1 + self._strength_as_decimal) ** (level - 1) - 1 + 1e-9) / self._strength_as_decimal)
        )


class _ProgressInfo(TypedDict):
    current_level: int
    current_level_xp: int
    current_xp: int
    next_level_xp: int
    is_maxed: bool


class _LevelXp(TypedDict):
    level: int
    xp: int


class InterpolateAbstractLevelUpper(AbstractLevelUpper):

    def __init__(self, level_to_xp_map: Dict[int, int]) -> None:
        self._xp_to_level: List[_LevelXp] = sorted(
            ({"level": level, "xp": xp} for level, xp in level_to_xp_map.items()),
            key=lambda entry: entry["xp"],
        )

    def current_level(self, xp: int) -> int:
        return self._find_progress_info(xp)["current_level"]

    def total_xp_required(self, xp: int) -> int:
        info = self._find_progress_info(xp)
        return info["next_level_xp"] - info["current_level_xp"]

    def progress(self, xp: int) -> int:
        info = self._find_progress_info(xp)
        return info["current_xp"] - info["current_level_xp"]

    def progress_percentage(self, xp: int) -> int:
        info = self._find_progress_info(xp)
        total_required = info["next_level_xp"] - info["current_level_xp"]
        if total_required == 0:
            return 0
        return int(((info["current_xp"] - info["current_level_xp"]) / total_required) * 100)

    def xp_remaining(self, xp: int) -> int:
        info = self._find_progress_info(xp)
        return info["next_level_xp"] - info["current_xp"]

    def is_maxed(self, xp: int) -> bool:
        return self._find_progress_info(xp)["is_maxed"]

    def max_level(self) -> int:
        return self._find_progress_info(self.max_xp())["current_level"]

    def max_xp(self) -> int:
        if len(self._xp_to_level) == 0:
            return 0
        return self._xp_to_level[-1]["xp"]

    def _find_progress_info(self, xp: int) -> _ProgressInfo:
        if len(self._xp_to_level) == 0:
            return {
                "current_level": 1,
                "current_level_xp": 0,
                "current_xp": 0,
                "next_level_xp": 0,
                "is_maxed": True,
            }

        current_xp = self.current_xp(xp)
        last = self._xp_to_level[-1]
        if current_xp >= last["xp"]:
            return {
                "current_level": last["level"],
                "current_level_xp": last["xp"],
                "current_xp": last["xp"],
                "next_level_xp": last["xp"],
                "is_maxed": True,
            }

        floor: _LevelXp = {"level": 1, "xp": 0}
        ceil: _LevelXp = self._xp_to_level[0]
        for entry in self._xp_to_level:
            if entry["xp"] <= current_xp:
                floor = entry
                continue
            ceil = entry
            break

        level_difference = ceil["level"] - floor["level"]
        xp_difference = ceil["xp"] - floor["xp"]
        xp_per_level = xp_difference / level_difference
        interpolation_progress = current_xp - floor["xp"]
        level_steps = min(
            max(int(interpolation_progress / xp_per_level), 0),
            level_difference - 1,
        )

        current_level = floor["level"] + level_steps
        current_level_xp = floor["xp"] + int(xp_per_level * level_steps)

        if level_steps == level_difference - 1:
            next_level_xp = ceil["xp"]
        else:
            next_level_xp = floor["xp"] + int(xp_per_level * (level_steps + 1))
            if current_xp >= next_level_xp:
                level_steps += 1
                current_level = floor["level"] + level_steps
                current_level_xp = floor["xp"] + int(xp_per_level * level_steps)
                next_level_xp = (
                    ceil["xp"]
                    if level_steps == level_difference
                    else floor["xp"] + int(xp_per_level * (level_steps + 1))
                )

        return {
            "current_level": current_level,
            "current_level_xp": current_level_xp,
            "current_xp": current_xp,
            "next_level_xp": next_level_xp,
            "is_maxed": False,
        }


class LevelUpper:

    @staticmethod
    def linear(step_size: int, max_level: int) -> LinearAbstractLevelUpper:

        return LinearAbstractLevelUpper(step_size, max_level)

    @staticmethod
    def interpolate(level_to_xp_map: Dict[int, int]) -> InterpolateAbstractLevelUpper:

        return InterpolateAbstractLevelUpper(level_to_xp_map)

    @staticmethod
    def exponential(
        initial_xp: int, strength: int, max_level: int
    ) -> ExponentialAbstractLevelUpper:

        return ExponentialAbstractLevelUpper(initial_xp, strength, max_level)
