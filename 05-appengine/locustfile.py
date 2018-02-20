from locust import HttpLocust, TaskSet, task

class FlaskSiteTask(TaskSet):
    @task
    def index(self):
        self.client.get("/")


class FlaskSiteUser(HttpLocust):
    task_set = FlaskSiteTask
    min_wait = 5000
    max_wait = 5000