import services
from sims.sim import Sim
from sims4.resources import Types

from smp4.utils.native.injector import inject

SMP4_AFFORDANCES = (
    15046892415517235728,  # simmy_chatdialog_4162018
)


@inject(Sim, 'on_add')
def _inject_smp4_affordances_to_sim_instance(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)

    global SMP4_AFFORDANCES

    affordance_instances = list()
    affordance_manager = services.get_instance_manager(Types.INTERACTION)

    for affordance_id in SMP4_AFFORDANCES:
        affordance_instance = affordance_manager.get(affordance_id)

        if affordance_instance is None:
            continue

        affordance_instances.append(affordance_instance)

    self._super_affordances = self._super_affordances + tuple(affordance_instances)

    return result
