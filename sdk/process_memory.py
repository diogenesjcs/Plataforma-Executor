from urllib.error import HTTPError
from sdk import settings, models
from sdk.utils import HttpClient


def create_memory(process):
    result = HttpClient.post(
        f"{settings.PROCESS_MEMORY_URL}:{settings.PROCESS_MEMORY_PORT}/{process['id']}/create")

    return not result.has_error
