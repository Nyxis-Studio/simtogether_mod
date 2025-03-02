import ts4mp.utils.native.injector as injector
from ts4mp.core import multiplayer_client, multiplayer_server
import services
import sims4
from  ts4mp.core.overrides.override_functions import override_functions_depending_on_client_or_not
import ts4mp.configs.server_config
import ts4mp.utils.native.injector
from ts4mp.core.csn import show_server_host_attempt
from ts4mp.configs.server_config import MULTIPLAYER_MOD_ENABLED
from ts4mp.debug.log import ts4mp_log

if MULTIPLAYER_MOD_ENABLED:
    is_client = False
    client_instance = None
    server_instance = None

    current_lot_id = 0


    def setup(client_arg: bool, client_host = 0, client_port = 0):
        global current_lot_id
        global is_client
        global client_instance
        global server_instance
        is_client = client_arg
        if is_client:
            #if there's already an existing client or server, it means the player is trying to reconnect
            if client_instance is not None:
                client_instance.kill()
                client_instance = None

            client_instance = multiplayer_client.Client()
            client_instance.host = client_host
            client_instance.port = client_port
            client_instance.send()
            client_instance.listen()

            override_functions_depending_on_client_or_not(is_client)
        else:
            #if there's already an existing client or server, it means the player is trying to reconnect
            if server_instance is not None:
                server_instance.kill()
                server_instance = None

            server_instance = multiplayer_server.Server()
            server_instance.heartbeat()

            server_instance.listen()
            server_instance.send()

            override_functions_depending_on_client_or_not(is_client)

    def on_successful_client_connect():
        override_functions_depending_on_client_or_not(True)

    @sims4.commands.Command('mp.connect', command_type=sims4.commands.CommandType.Live)
    def connect(_connection=None):
        setup(True, ts4mp.configs.server_config.HOST, ts4mp.configs.server_config.PORT)

    @sims4.commands.Command('mp.host', command_type=sims4.commands.CommandType.Live)
    def host(_connection=None):
        ts4mp_log("host", "Starting server....")
        setup(False)
        show_server_host_attempt()

    @injector.inject(services, "stop_global_services")
    def stop_global_services(original):
        global client_instance
        if client_instance is not None:
            client_instance.kill()

        global server_instance
        if server_instance is not None:
            server_instance.kill()
        original()

