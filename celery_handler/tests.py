__author__ = "Deepak Verma"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Deepak Verma"
__email__ = "dverma.work@gmail.com"
__status__ = "Development"


from django.test import TestCase, SimpleTestCase
from django.core.urlresolvers import resolve, reverse
from django.conf import settings

from core.constants import *

from celery_handler.tasks import ETS


class ETSCeleryTaskTestCase(TestCase):
    """
    To access django request/response use self.client (from django.test import Client)
    This Test Suite validates all use case of User authentication
    """

    def setUp(self):
        self.task_args = {'client_instance': 11, 'user_instance': 523}
        self.ets_task = ETS()

    def _inner_task_data_point(self, data_key):
        try:
            self.task_args['data_key'] = data_key
            res = self.ets_task.run(**self.task_args)
        except Exception as ex:
            self.assertFalse(True, msg=str(ex))

    def test_task_missing_arguments(self):
        """Running test_task_missing_arguments"""
        response = self.client.post(reverse("task_handler"), {})
        self.assertEqual(response.json()['code'], CELERY_NOT_ENOUGH_ARGUMENTS)
        response = self.client.post(reverse("task_handler"), {'data_key': ''})
        self.assertEqual(response.json()['code'], CELERY_NOT_ENOUGH_ARGUMENTS)
        response = self.client.post(reverse("task_handler"), {'data_key':'', 'client_instance':'', 'user_instance': ''})
        self.assertEqual(response.json()['code'], CELERY_NOT_ENOUGH_ARGUMENTS)
        response = self.client.post(reverse("task_handler"), {'data_key':'ETS', 'client_instance':'', 'user_instance': ''})
        self.assertEqual(response.json()['code'], CELERY_NOT_ENOUGH_ARGUMENTS)

        response = self.client.post(reverse("task_handler"), {'data_key':'ETS', 'client_instance':'1231', 'user_instance': '123'})
        self.assertEqual(response.json()['code'], CELERY_TASKS_ADDED)

    def test_ETS_EXCEPTION_NEW(self):
        """Running test_ETS_EXCEPTION_NEW """
        self._inner_task_data_point('ETS_EXCEPTION_NEW')

    def test_ETS_EXCEPTION_EARLY_ALERT(self):
        """Running test_ETS_EXCEPTION_EARLY_ALERT """
        self._inner_task_data_point('ETS_EXCEPTION_EARLY_ALERT')

    def test_ETS_EXCEPTION_UNRESOLVED(self):
        """Running test_ETS_EXCEPTION_UNRESOLVED """
        self._inner_task_data_point('ETS_EXCEPTION_UNRESOLVED')

    def test_ETS_PENDING_PTC(self):
        """Running test_ETS_PENDING_PTC """
        self._inner_task_data_point('ETS_PENDING_PTC')

    def test_ETS_PENDING_ACTIVITY_REQUEST(self):
        """Running test_ETS_PENDING_ACTIVITY_REQUEST """
        self._inner_task_data_point('ETS_PENDING_ACTIVITY_REQUEST')

    def test_LOCKED_USER(self):
        """Running test_LOCKED_USER """
        self._inner_task_data_point('LOCKED_USER')

    def test_ETS_WHISTLEBLOWER_ALERT(self):
        """Running test_ETS_WHISTLEBLOWER_ALERT """
        self._inner_task_data_point('ETS_WHISTLEBLOWER_ALERT')

    def test_ETS_CASES_COMMUNICATION(self):
        """Running test_ETS_CASES_COMMUNICATION """
        self._inner_task_data_point('ETS_CASES_COMMUNICATION')

    def test_ETS_EMP_MOST_EXCEPTION_12(self):
        """Running test_ETS_EMP_MOST_EXCEPTION_12 """
        self._inner_task_data_point('ETS_EMP_MOST_EXCEPTION_12')

    def test_ETS_MOST_TRADED_SECURITY_3(self):
        """Running test_ETS_MOST_TRADED_SECURITY_3 """
        self._inner_task_data_point('ETS_MOST_TRADED_SECURITY_3')

    def test_ETS_EMP_MOST_TRADE_DENIED(self):
        """Running test_ETS_EMP_MOST_TRADE_DENIED """
        self._inner_task_data_point('ETS_EMP_MOST_TRADE_DENIED')

    def test_ETS_EMP_MOST_DENIED_ACTIVITY_REQUEST(self):
        """Running test_ETS_EMP_MOST_DENIED_ACTIVITY_REQUEST """
        self._inner_task_data_point('ETS_EMP_MOST_DENIED_ACTIVITY_REQUEST')

    def test_ETS_EMP_highest_Potential_Harm(self):
        """Running test_ETS_EMP_highest_Potential_Harm """
        self._inner_task_data_point('ETS_EMP_highest_Potential_Harm')

    def test_ETS_EMP_GROUP_MOST_EXCEPTION(self):
        """Running test_ETS_EMP_GROUP_MOST_EXCEPTION """
        self._inner_task_data_point('ETS_EMP_GROUP_MOST_EXCEPTION')

    def test_ETS_LARGEST_HOLDING_ALL_CLIENT(self):
        """Running test_ETS_LARGEST_HOLDING_ALL_CLIENT """
        self._inner_task_data_point('ETS_LARGEST_HOLDING_ALL_CLIENT')

    def test_ETS_LARGEST_HOLDING_ALL_EMP(self):
        """Running test_ETS_LARGEST_HOLDING_ALL_EMP """
        self._inner_task_data_point('ETS_LARGEST_HOLDING_ALL_EMP')

    def test_ETS_MOST_ACTIVE_TRADER(self):
        """Running test_ETS_MOST_ACTIVE_TRADER """
        self._inner_task_data_point('ETS_MOST_ACTIVE_TRADER')

    def test_ETS_MOST_Political_Contribution(self):
        """Running test_ETS_MOST_Political_Contribution """
        self._inner_task_data_point('ETS_MOST_Political_Contribution')

    def test_ETS_MOST_TRADE_GROUP(self):
        """Running test_ETS_MOST_TRADE_GROUP """
        self._inner_task_data_point('ETS_MOST_TRADE_GROUP')

    def test_ETS_CERTIFICATION_PENDING(self):
        """Running test_ETS_CERTIFICATION_PENDING """
        self._inner_task_data_point('ETS_CERTIFICATION_PENDING')

    def test_ETS_CERTIFICATION_PAST_DUE(self):
        """Running test_ETS_CERTIFICATION_PAST_DUE """
        self._inner_task_data_point('ETS_CERTIFICATION_PAST_DUE')

    def test_ETS_CERTIFICATION_REVIEW(self):
        """Running test_ETS_CERTIFICATION_REVIEW """
        self._inner_task_data_point('ETS_CERTIFICATION_REVIEW')

    def test_ETS_HOLDING_CONFIRMATION_PAST_DUE(self):
        """Running test_ETS_HOLDING_CONFIRMATION_PAST_DUE """
        self._inner_task_data_point('ETS_HOLDING_CONFIRMATION_PAST_DUE')


# data_keys = 'ETS_EXCEPTION_NEW,ETS_EXCEPTION_EARLY_ALERT,ETS_EXCEPTION_UNRESOLVED,ETS_PENDING_PTC,' \
#          'ETS_PENDING_ACTIVITY_REQUEST,LOCKED_USER,ETS_WHISTLEBLOWER_ALERT,ETS_CASES_COMMUNICATION,' \
#          'ETS_EMP_MOST_EXCEPTION_12,ETS_MOST_TRADED_SECURITY_3,ETS_EMP_MOST_TRADE_DENIED,' \
#          'ETS_EMP_MOST_DENIED_ACTIVITY_REQUEST,ETS_EMP_highest_Potential_Harm,ETS_EMP_GROUP_MOST_EXCEPTION,' \
#          'ETS_LARGEST_HOLDING_ALL_CLIENT,ETS_LARGEST_HOLDING_ALL_EMP,ETS_MOST_ACTIVE_TRADER,' \
#          'ETS_MOST_Political_Contribution,ETS_MOST_TRADE_GROUP,ETS_CERTIFICATION_PENDING,' \
#          'ETS_CERTIFICATION_PAST_DUE,ETS_CERTIFICATION_REVIEW,ETS_HOLDING_CONFIRMATION_PAST_DUE'
#
# template_test_fun = '''
#     def test_{data_key}(self):
#        """Running test_{data_key} """
#         self._inner_task_data_point('{data_key}')
#     '''
# for data_key in data_keys.split(','):
#     print(template_test_fun.format(data_key=data_key))
