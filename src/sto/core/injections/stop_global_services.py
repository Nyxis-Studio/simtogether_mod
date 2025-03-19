import sto.utils.native.injector as injector
import services


@injector.inject(services, "stop_global_services")
def stop_global_services(original):
    global MP_INSTANCE
    if MP_INSTANCE is not None:
        MP_INSTANCE.kill()

    original()
