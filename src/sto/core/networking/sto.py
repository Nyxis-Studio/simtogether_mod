import sto.core.networking.protocolbuffers.Sto_pb2 as StoProtocols


def build_sto_message(operation):
    sto_update = StoProtocols.StoUpdate()
    entry = sto_update.entries.add()
    sto_operation = StoProtocols.Operation()
    operation.write(sto_operation)
    entry.operation_list.operations.append(sto_operation)

    return sto_update
