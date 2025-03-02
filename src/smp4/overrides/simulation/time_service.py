import time_service
import smp4.core.mp_sync
import time
import services

from time_service import logger
from smp4.debug.log import debug_log


def update(self, time_slice=True):
    debug_log("simulate", "Client is online?: {}".format(smp4.core.mp_sync.client_online), force=False)

    if smp4.core.mp_sync.client_online:
        debug_log("simulate", "Client is online?: {}".format(smp4.core.mp_sync.client_online), force=True)
        return

    max_time_ms = self.MAX_TIME_SLICE_MILLISECONDS if time_slice else None
    t1 = time.time()
    result = self.sim_timeline.simulate(services.game_clock_service().now(), max_time_ms=max_time_ms)
    t2 = time.time()

    debug_log("simulate", "{} ms".format((t2 - t1) * 1000), force=True)
    if not result:
        logger.debug('Did not finish processing Sim Timeline. Current element: {}', self.sim_timeline.heap[0])
    result = self.wall_clock_timeline.simulate(services.server_clock_service().now())
    if not result:
        logger.error('Too many iterations processing wall-clock Timeline. Likely culprit: {}', self.wall_clock_timeline.heap[0])


def override_functions_depending_on_client_or_not(is_client):
    if is_client:
        time_service.TimeService.update = update