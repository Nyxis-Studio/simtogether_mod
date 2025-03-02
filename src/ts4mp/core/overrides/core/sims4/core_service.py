import ts4mp.core.mp_sync
import game_services
import services
import sims4.commands
import time

from ts4mp.utils.native.decorator import decorator
from sims4 import core_services
from ts4mp.core.mp_sync import outgoing_lock, outgoing_commands, client_sync, server_sync
from server_commands.clock_commands import set_speed, request_pause, unrequest_pause, toggle_pause_unpause
from server_commands.interaction_commands import has_choices, generate_choices, generate_phone_choices, select_choice, cancel_mixer_interaction, cancel_super_interaction, push_interaction
from server_commands.lighting_commands import set_color_and_intensity
from server_commands.sim_commands import set_active_sim
from server_commands.ui_commands import ui_dialog_respond, ui_dialog_pick_result, ui_dialog_text_input
from ts4mp.core.csn import mp_chat
from server_commands.career_commands import find_career, select_career
from ts4mp.debug.log import ts4mp_log
from server_commands.argument_helpers import  RequiredTargetParam
from ts4mp.utils.native.undecorated import undecorated


COMMAND_FUNCTIONS = {
    'interactions.has_choices'        : has_choices,
    'interactions.choices'            : generate_choices,
    'interactions.phone_choices'      : generate_phone_choices,
    'interactions.select'             : select_choice,
    'interactions.cancel'             : cancel_mixer_interaction,
    'interactions.cancel_si'          : cancel_super_interaction,
    'interactions.push'               : push_interaction,
    'clock.setspeed'                  : set_speed,
    'clock.request_pause'             : request_pause,
    'clock.pause'                     : request_pause,
    'clock.unrequest_pause'           : unrequest_pause,
    'clock.unpause'                   : unrequest_pause,
    'clock.toggle_pause_unpause'      : toggle_pause_unpause,
    'sims.set_active'                 : set_active_sim,
    'mp_chat'                         : mp_chat,
    'ui.dialog.respond'               : ui_dialog_respond,
    'ui.dialog.pick_result'           : ui_dialog_pick_result,
    'ui.dialog.text_input'            : ui_dialog_text_input,
    'lighting.set_color_and_intensity': set_color_and_intensity,
    "careers.find_career"             : find_career,
    "careers.select"                  : select_career
}

def on_tick_client():
    # On Tick override for the client.
    # If the service manager hasn't been initialized, return because we don't even have a client manager yet.
    # If we don't have any client, that means we aren't in a zone yet.
    # If we do have at least one client, that means we are in a zone and can sync information.
    service_manager = game_services.service_manager
    ts4mp.core.mp_sync.client_online = False

    if service_manager is None:
        return

    client_manager = services.client_manager()

    if client_manager is None:
        return

    client = client_manager.get_first_client()

    if client is None:
        return
    ts4mp.core.mp_sync.client_online = True

    client_sync()


def on_tick_server():
    # On Tick override for the client.
    # If the service manager hasn't been initialized, return because we don't even have a client manager yet.
    # If we don't have any client, that means we aren't in a zone yet.
    # If we do have at least one client, that means we are in a zone and can sync information.
    service_manager = game_services.service_manager
    if service_manager is None:
        return

    client_manager = services.client_manager()

    if client_manager is None:
        return

    client = client_manager.get_first_client()

    if client is None:
        return

    server_sync()

@decorator
def wrapper_client(func, *args, **kwargs):
    # Wrapper for functions that have their data needed to be sent to the server.
    # This is used for client commands so the server can respond.
    # For example, selecting a choice from the pie menu.
    # Only supports one multiplayer client at the moment.

    ts4mp_log("locks", "acquiring outgoing lock")

    with outgoing_lock:
        # TODO: You should not be referring to a global variable that is in a different module
        parsed_args = []
        for arg in args:
            if isinstance(arg, RequiredTargetParam):
                arg = arg.target_id
            parsed_args.append(arg)
        ts4mp_log("arg_handler", "\n" + str(func.__name__) + ", " + str(parsed_args) + "  " + str(kwargs), force=False)
        outgoing_commands.append("\n" + str(func.__name__) + ", " + str(parsed_args) + "  " + str(kwargs))
    # we sleep here so the networking threads can send the commands, if you remove this, it will make the response times
    # higher
    time.sleep(0.2)

    def do_nothing():
        pass

    return do_nothing

def override_functions_depending_on_client_or_not(is_client):
    if is_client:
        core_services.on_tick = on_tick_client
        
        for function_command_name, command_function in COMMAND_FUNCTIONS.items():
            sims4.commands.Command(function_command_name, command_type=sims4.commands.CommandType.Live)(wrapper_client(undecorated(command_function)))
    else:
        core_services.on_tick = on_tick_server
