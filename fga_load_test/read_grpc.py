import uuid
import time
import asyncio
import inspect
import requests

from grpclib.client import Channel
from locust.contrib.fasthttp import FastHttpUser
from locust import HttpUser, task, between, events, constant

from fga_load_test.constants import AUTH_HEADER, STORE_ID, FGA_API
from fga_load_test.models import GITHUB, SLACK, COMPASS, CONTROLPLANE
from fga_load_test.proto.openfga.v1 import OpenFGAServiceStub, TupleKey


requests.packages.urllib3.disable_warnings()


def stopwatch(func):
    """To be updated"""

    def wrapper(*args, **kwargs):
        """To be updated"""
        # get task's function name
        previous_frame = inspect.currentframe().f_back
        _, _, task_name, _, _ = inspect.getframeinfo(previous_frame)

        start = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            total = int((time.time() - start) * 1000)
            events.request.fire(
                request_type="TYPE",
                name=task_name,
                response_time=total,
                response_length=0,
                exception=e,
            )
        else:
            total = int((time.time() - start) * 1000)
            events.request.fire(
                request_type="TYPE",
                name=task_name,
                response_time=total,
                response_length=0,
            )
        return result

    return wrapper


class GithubRead(FastHttpUser):
    wait_time = constant(0)

    def on_start(self):
        self.client.verify = False

    @task
    @stopwatch
    def grpc_client_task(self):
        objects = "organization:openfga"
        relation = "owner"
        user = f"user:{str(uuid.uuid4())}"

        channel = Channel(host=FGA_API)
        fga = OpenFGAServiceStub(channel)
        response = asyncio.run(
            fga.check(
                store_id=STORE_ID,
                tuple_key=TupleKey(object=objects, relation=relation, user=user),
                authorization_model_id=GITHUB,
            )
        )
        print(40 * "#$#")
        print(response.allowed)
        print(response)
