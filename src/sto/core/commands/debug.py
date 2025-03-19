import sims4

from sto.debug.log import Logger


@sims4.commands.Command("net.info", command_type=sims4.commands.CommandType.Live)
def _get_network_info(_connection=None):
    output = sims4.commands.CheatOutput(_connection)

    from sto.core.networking.client import Client

    client = Client()

    log(output, "Client host: {}".format(client.host))
    log(output, "Client port: {}".format(client.port))
    log(output, "Client alive: {}".format(client.alive))
    log(output, "Client connected: {}".format(client.is_connected()))
    log(output, "Client stop event is set: {}".format(client.stop_event.is_set()))
    log(
        output,
        "Client send stop event is set: {}".format(client.send_stop_event.is_set()),
    )
    log(
        output,
        "Client listen stop event is set: {}".format(client.listen_stop_event.is_set()),
    )

    from sto.core.networking.messages import IncomingMessages, OutgoingMessages

    log(output, "Client outgoing messages: {}".format(len(OutgoingMessages().messages)))
    log(output, "Client incoming messages: {}".format(len(IncomingMessages().messages)))


@sims4.commands.Command("net.threads", command_type=sims4.commands.CommandType.Live)
def _get_network_threads(_connection=None):
    output = sims4.commands.CheatOutput(_connection)

    from sto.core.networking.client import Client

    client = Client()

    if client.listen_thread is None:
        log(output, "Client listen thread is None")
    else:
        log(
            output,
            "Client listen thread is alive?: {}".format(
                client.listen_thread.is_alive()
            ),
        )

    if client.send_thread is None:
        log(output, "Client send thread is None")
    else:
        log(
            output,
            "Client send thread is alive?: {}".format(client.send_thread.is_alive()),
        )

    if client.heartbeat_thread is None:
        log(output, "Client heartbeat thread is None")
    else:
        log(
            output,
            "Client heartbeat thread is alive?: {}".format(
                client.heartbeat_thread.is_alive()
            ),
        )


def log(output, msg):
    Logger().info(msg)
    output(msg)
