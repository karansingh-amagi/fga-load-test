import uuid
import random
from locust import HttpUser, task, between
from fga_load_test.constants import AUTH_HEADER, STORE_ID
from fga_load_test.models import GITHUB, SLACK, COMPASS, CONTROLPLANE


class GithubWrite(HttpUser):
    wait_time = between(1, 5)

    @task
    def write(self):
        objects = "organization:openfga"
        relation = "owner"
        user = ["karan", "roshan", "chaitanya"]
        write_tuple = {
            "writes": {
                "tuple_keys": [
                    {
                        "object": objects,
                        "relation": relation,
                        # "user": f"user:{str(uuid.uuid4())}",
                        "user": random.choice(user),
                    },
                ]
            },
            "authorization_model_id": GITHUB,
        }
        response = self.client.post(
            url=f"/stores/{STORE_ID}/write", headers=AUTH_HEADER, json=write_tuple
        )
        print(f"STATUS: {response.status_code}\tRESPONSE: {response.json()}")

    def on_start(self):
        self.client.verify = False
