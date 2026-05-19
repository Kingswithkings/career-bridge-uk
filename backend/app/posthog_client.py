import atexit

from posthog import Posthog

from .config import POSTHOG_API_KEY, POSTHOG_HOST

posthog_client = Posthog(
    project_api_key=POSTHOG_API_KEY,
    host=POSTHOG_HOST,
    enable_exception_autocapture=True,
)

atexit.register(posthog_client.shutdown)
