import clock
import sims4

from sto.configs.server_config import MULTIPLAYER_MOD_ENABLED
from clock import ClockSpeedMode, GameSpeedChangeSource
from sto.core.networking.client import Client

logger = sims4.log.Logger("Clock", default_owner="trevor")


def set_clock_speed(
    self, speed, source=GameSpeedChangeSource.GAMEPLAY, reason="", immediate=False
) -> bool:
    if Client().is_connected():
        speed = ClockSpeedMode.PAUSED
        reason = "Multiplayer not connected"

    if speed not in ClockSpeedMode.values:
        logger.error("Attempting to set clock speed to something invalid: {}", speed)
        return False
    logger.debug(
        "set_clock_speed CALLED ...\n    speed: {}, change_source: {}, reason: {}",
        speed,
        source,
        reason,
    )
    self.speed_controllers[source][:] = [
        request
        for request in self.speed_controllers[source]
        if request.speed == ClockSpeedMode.SUPER_SPEED3
    ]
    if speed != ClockSpeedMode.SPEED3:
        self.speed_controllers[source].push_speed(speed, reason=str(reason))
    else:
        for speed_request in self.game_speed_requests_gen():
            if not speed_request.validity_check is None:
                if speed_request.validity_check():
                    secondary_speed = speed_request.speed
                    break
            secondary_speed = speed_request.speed
            break
        secondary_speed = None
        if secondary_speed != ClockSpeedMode.SUPER_SPEED3:
            self.speed_controllers[source].push_speed(speed, reason=str(reason))
    self._update_speed(immediate=immediate)
    logger.debug(
        "set_clock_speed SUCCEEDED. speed: {}, change_source: {}, reason: {}",
        speed,
        source,
        reason,
    )
    return True


if MULTIPLAYER_MOD_ENABLED:
    clock.GameClock.set_clock_speed = set_clock_speed
