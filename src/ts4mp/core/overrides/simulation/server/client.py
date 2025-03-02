import services
import server.client
import omega
from protocolbuffers.Distributor_pb2 import ViewUpdate

from server.client import logger
from distributor.system import Distributor
from ts4mp.configs.server_config import MULTIPLAYER_MOD_ENABLED
from objects import ALL_HIDDEN_REASONS
from protocolbuffers import Sims_pb2
from distributor.ops import GenericProtocolBufferOp, Heartbeat, SetGameTime
from distributor.rollback import ProtocolBufferRollback
from ts4mp.core.mp_sync import ProtocolBufferMessage, outgoing_lock, outgoing_commands
from protocolbuffers.DistributorOps_pb2 import Operation

from ts4mp.debug.log import ts4mp_log

def send_selectable_sims_update(self):
    msg = Sims_pb2.UpdateSelectableSims()

    for sim_info in self._selectable_sims:
        with ProtocolBufferRollback(msg.sims) as new_sim:
            new_sim.id = sim_info.sim_id
            career = sim_info.career_tracker.get_currently_at_work_career()
            if sim_info.career_tracker is None:
                logger.error('CareerTracker is None for selectable Sim {}'.format(sim_info))
            else:
                career = sim_info.career_tracker.get_currently_at_work_career()
                new_sim.at_work = career is not None and not career.is_at_active_event
            new_sim.is_selectable = sim_info.get_is_enabled_in_skewer()
            (selector_visual_type, career_category) = self._get_selector_visual_type(sim_info)
            new_sim.selector_visual_type = selector_visual_type

            if career_category is not None:
                new_sim.career_category = career_category

            new_sim.can_care_for_toddler_at_home = sim_info.can_care_for_toddler_at_home

            if not sim_info.is_instanced(allow_hidden_flags=ALL_HIDDEN_REASONS):
                new_sim.instance_info.zone_id = sim_info.zone_id
                new_sim.instance_info.world_id = sim_info.world_id
                new_sim.firstname = sim_info.first_name
                new_sim.lastname = sim_info.last_name
                zone_data_proto = services.get_persistence_service().get_zone_proto_buff(sim_info.zone_id)

                if zone_data_proto is not None:
                    new_sim.instance_info.zone_name = zone_data_proto.name
    ts4mp_log("debugging", "client id is: {}".format(self.id))
    distributor_instance = Distributor.instance().get_client(self.id)
    distributor_instance.add_op_with_no_owner(GenericProtocolBufferOp(Operation.SELECTABLE_SIMS_UPDATE, msg))

def on_add(self):
    # We override the on_add function of the clients so we can add the stand-in client at the same time. Only supports  one
    # multiplayer client at the moment, which has the id of 1000.
    if self.id != 1000:
        #this block of code is triggered to create another client if this client is a "real" client

        account = server.account.Account(865431, "Elder Price")
        new_client = services.client_manager().create_client(1000, account, 0)
        for sim_info in self._selectable_sims:
            new_client._selectable_sims.add_selectable_sim_info(sim_info)
            new_client.set_next_sim()

    if self._account is not None:
        self._account.register_client(self)

    for sim_info in self._selectable_sims:
        self.on_sim_added_to_skewer(sim_info)

    distributor_instance = Distributor.instance()
    distributor_instance.add_object(self)
    distributor_instance.add_client(self)

    self.send_selectable_sims_update()
    self.selectable_sims.add_watcher(self, self.send_selectable_sims_update)

def on_remove(self):
    # We override the on_remove function of the client so we can remove the stand-in client at the same time.
    # Only supports one multiplayer client at the moment, which has the id of 1000.
    if self.active_sim is not None:
        self._set_active_sim_without_field_distribution(None)

    if self._account is not None:
        self._account.unregister_client(self)

    for sim_info in self._selectable_sims:
        self.on_sim_removed_from_skewer(sim_info)

    self.selectable_sims.remove_watcher(self)

    distributor_instance = Distributor.instance()
    distributor_instance.remove_client(self)

    self._selectable_sims = None
    self.active = False

    if self.id != 1000:
        Distributor.instance().remove_client_from_id(1000)
        client_manager = services.client_manager()
        client = client_manager.get(1000)
        client_manager.remove(client)

def send_message_server(self, msg_id, msg):
    # Send message override for the server.
    # This overrides it so any message for a client with an id of 1000 gets packed into a Message and is placed in the outgoing_commands list for
    # sending out to the multiplayer clients.
    # Only supports one multiplayer client at the moment.

    #ts4mp_log("network", "Sending message to client id: {}".format(self.id))

    log_update_view_protocol = None

    if isinstance(msg, ViewUpdate):
        for entry in msg.entries:
            for operation in entry.operation_list.operations:
                if operation.type == log_update_view_protocol:
                    ts4mp_log("network", self.id)
                    ts4mp_log("network", operation)

    if self.id != 1000:
        if self.active:
            omega.send(self.id, msg_id, msg.SerializeToString())
        # ts4mp_log_debug("msg", msg)
    else:
        message = ProtocolBufferMessage(msg_id, msg.SerializeToString())
        ts4mp_log("locks", "acquiring outgoing lock")

        # We use a lock here because outgoing_commands is also being altered by the client socket thread.
        with outgoing_lock:
            outgoing_commands.append(message)
        #ts4mp_log("network", "Queueing outgoing command for {}".format(self.id))

        ts4mp_log("locks", "releasing outgoing lock")

def send_message_client(self, msg_id, msg):
    # Send Message override for the client.
    # We don't want any of the original server sending stuff to the client.
    # So we override it to do absolutely nothing.
    pass

if MULTIPLAYER_MOD_ENABLED:
    server.client.Client.send_selectable_sims_update = send_selectable_sims_update
    server.client.Client.on_add = on_add
    server.client.Client.on_remove = on_remove
    server.client.Client.send_message = send_message_server

def override_functions_depending_on_client_or_not(is_client):
    if is_client:
        server.client.Client.send_message = send_message_client