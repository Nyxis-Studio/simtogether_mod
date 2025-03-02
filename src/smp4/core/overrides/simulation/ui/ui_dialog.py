import ui.ui_dialog

from smp4.configs.server_config import MULTIPLAYER_MOD_ENABLED
from distributor.system import Distributor
from smp4.debug.log import debug_log

def distribute_dialog(self, dialog_type, dialog_msg, immediate=False):
    distributor_instance = Distributor.instance()
    distributor_to_send_to = distributor_instance.get_distributor_with_active_sim_matching_sim_id(dialog_msg.owner_id)
    distributor_instance.add_event_for_client(distributor_to_send_to, dialog_type, dialog_msg, immediate)

    if dialog_msg:
        debug_log("events", "{}".format(str(dialog_msg.owner_id)))

if MULTIPLAYER_MOD_ENABLED:
    ui.ui_dialog.UiDialogBase.distribute_dialog = distribute_dialog