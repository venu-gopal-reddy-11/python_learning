from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def my_task(self):
        self.client.get("/")


# to run file " locust -f locustfile.py"

