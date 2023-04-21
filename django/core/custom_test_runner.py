import time
from django.test.runner import DiscoverRunner
from .tools import drop_test_db

class CustomTestRunner(DiscoverRunner):

    def setup_databases(self, *args, **kwargs):
        drop_test_db()
        time.sleep(1)
        return super().setup_databases(*args, **kwargs)
        

