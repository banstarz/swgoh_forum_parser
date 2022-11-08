import pytest
from requests.exceptions import RequestException
from swgoh_forum_parser.parser.request_decorators import retry, delay_request


class TestRetry:
    retries: int = 0

    @pytest.fixture(autouse=True)
    def mocker_sleep(self, mocker):
        mocker.patch('time.sleep', side_effect=self.count_retries)
        return

    def test_no_retry_on_success(self, mocker_sleep):
        response = self.success_response()

        assert self.retries == 0
        assert response == 'success'

    def test_retry_on_request_exception(self, mocker_sleep):
        self.request_exception_raiser()

        assert self.retries == 4

    def test_no_retry_on_another_exception(self, mocker_sleep):

        with pytest.raises(ValueError):
            self.another_exception_raiser()

        assert self.retries == 0

    def count_retries(self, *args, **kwargs) -> None:
        self.retries += 1

    @retry(4)
    def request_exception_raiser(self):
        raise RequestException

    @retry(3)
    def another_exception_raiser(self):
        raise ValueError

    @retry(5)
    def success_response(self):
        return 'success'


class TestDelay:
    count_sleep: int = 0
    sleep_time: float = 0

    @pytest.fixture(autouse=True)
    def mocker_sleep(self, mocker):
        mocker.patch('time.sleep', side_effect=self.count_retries)
        return

    def test_delay(self, mocker_sleep):
        response = self.success_response()

        assert self.count_sleep == 1
        assert self.sleep_time <= 10

    def test_response(self, mocker_sleep):
        response = self.success_response()

        assert response == 'success'

    def count_retries(self, seconds) -> None:
        self.count_sleep += 1
        self.sleep_time = seconds

    @delay_request(10)
    def success_response(self):
        return 'success'
