import math
from dataclasses import dataclass
from . import Operation


@dataclass
class EpsResult:
    min: int
    max: int
    average: int


class EventsPerSecond(Operation):
    async def _perform(self):
        intervals = {}
        async for line in self._reader.read():
            item = self._entity_factory.str_to_entity(line)
            _intv = self.get_interval(item.timestamp)
            if _intv not in intervals:
                intervals[_intv] = 1
            else:
                intervals[_intv] += 1
        interval_vals = intervals.values()
        return EpsResult(
            min=min(interval_vals),
            max=max(interval_vals),
            average=math.ceil(sum(interval_vals) / len(interval_vals)) if interval_vals else 0
        )

    def get_interval(self, timestamp):
        return int(timestamp)


class EventsPerMinute(EventsPerSecond):
    def get_interval(self, timestamp):
        return int(timestamp / 60)
