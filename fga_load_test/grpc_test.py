import uuid
import asyncio
from grpclib.client import Channel
from fga_load_test.proto.openfga.v1 import TupleKey, OpenFGAServiceStub
from fga_load_test.constants import FGA_API, STORE_ID
from fga_load_test.models import GITHUB


def grpc_client_task():
    objects = "organization:openfga"
    relation = "owner"
    user = f"user:{str(uuid.uuid4())}"

    channel = Channel(
        host="fga.controlplane-non-prod.iota.amagi.tv.iota.amagi.tv", port=8081
    )
    fga = OpenFGAServiceStub(channel)
    response = asyncio.get_event_loop().run_until_complete(
        fga.check(
            store_id=STORE_ID,
            tuple_key=TupleKey(object=objects, relation=relation, user=user),
            authorization_model_id=GITHUB,
        )
    )
    print(40 * "#$#")
    print(response.allowed)
    print(response)


grpc_client_task()
