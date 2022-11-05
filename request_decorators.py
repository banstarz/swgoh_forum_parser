import requests
import time
import random
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def retry(max_retries):
    def decorator(func):
        def retry_wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                logger.info(f'Trying to get content. {attempts} attempt')
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    logger.warning(e)
                    attempts += 1
                    time.sleep(random.randint(10, 25))

        return retry_wrapper
    return decorator


def delay_request(max_sleep_time=3):
    def decorator(func):
        def wait_wrapper(*args, **kwargs):
            delay_seconds = random.random() * max_sleep_time
            logger.debug(f'Sleeping for {delay_seconds} seconds')
            time.sleep(delay_seconds)
            return func(*args, **kwargs)

        return wait_wrapper
    return decorator
