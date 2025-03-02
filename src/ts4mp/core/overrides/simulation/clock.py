import clock

from clock import GameSpeedChangeSource

from ts4mp.configs.server_config import MULTIPLAYER_MOD_ENABLED

def push_speed(self, speed, source=GameSpeedChangeSource.GAMEPLAY, validity_check=None, reason='', immediate=False):
    if source == GameSpeedChangeSource.GAMEPLAY:
        request = self.speed_controllers[source].push_speed(speed, reason=str(reason), validity_check=validity_check)
        self._update_speed(immediate=immediate)

        return request

    return None

if MULTIPLAYER_MOD_ENABLED:
    clock.GameClock.push_speed = push_speed