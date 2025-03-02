import distributor.distributor_service
import animation.arb
from ts4mp.core.overrides.simulation.distributor import system as system_distributor

from ts4mp.configs.server_config import MULTIPLAYER_MOD_ENABLED

def start(self):
    # Override the original function with one that creates a "SystemDistributor" instead of a regular old Distributor.
    animation.arb.set_tag_functions(distributor.system.get_next_tag_id, distributor.system.get_current_tag_set)
    distributor.system._distributor_instance = system_distributor.Distributor()

if MULTIPLAYER_MOD_ENABLED:
    distributor.distributor_service.DistributorService.start = start