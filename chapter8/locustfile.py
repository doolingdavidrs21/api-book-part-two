import time
from locust import User, task, between, events
from swcpy import SWCClient, SWCConfig

class APIUser(User):
    # Simulate a user waiting between 1 and 3 seconds between tasks
    wait_time = between(1, 3)

    def on_start(self):
        """
        Runs once for every simulated user when they start.
        We initialize the SDK here using your exact working snippet.
        """
        # 1. Point the config to your AWS URL
        aws_url = "https://aws-api-container.xnkp6vj8k4sar.us-west-2.cs.amazonlightsail.com"

        # 2. Initialize the client
        # We store it in 'self' so the task below can use it
        config = SWCConfig(swc_base_url=aws_url, backoff=False)
        self.client = SWCClient(config)

    @task
    def get_leagues(self):
        """
        The actual test task. We wrap the SDK call in a timer
        so Locust knows how long it took.
        """
        start_time = time.time()
        try:
            # --- The actual SDK Call ---
            self.client.list_leagues()
            # ---------------------------

            # Calculate duration in milliseconds
            total_time = int((time.time() - start_time) * 1000)

            # Report SUCCESS to Locust
            events.request.fire(
                request_type="SDK",
                name="list_leagues",
                response_time=total_time,
                response_length=0,
                exception=None,
            )

        except Exception as e:
            # Calculate duration
            total_time = int((time.time() - start_time) * 1000)

            # Report FAILURE to Locust
            events.request.fire(
                request_type="SDK",
                name="list_leagues",
                response_time=total_time,
                exception=e,
            )