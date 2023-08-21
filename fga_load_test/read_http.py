# import uuid
import random
import requests

from locust import HttpUser, task, between

from fga_load_test.constants import AUTH_HEADER, STORE_ID
from fga_load_test.models import GITHUB, SLACK, COMPASS, CONTROLPLANE

requests.packages.urllib3.disable_warnings()


class GithubRead(HttpUser):
    wait_time = between(1, 5)

    @task
    def read(self):
        objects = "organization:openfga"
        relation = "owner"
        user = ["karan", "roshan", "chaitanya"]
        read_tuple = {
            "tuple_key": {
                "object": objects,
                "relation": relation,
                # "user": f"user:{str(uuid.uuid4())}",
                "user": random.choice(user),
            },
            "authorization_model_id": GITHUB,
        }
        response = self.client.post(
            url=f"/stores/{STORE_ID}/check", headers=AUTH_HEADER, json=read_tuple
        )
        print(f"STATUS: {response.status_code}\tRESPONSE: {response.text}")

    def on_start(self):
        self.client.verify = False
