import asyncio

import httpx


async def fetch_with_retry(client, url, retries=3, delay=1):
    """
    Attempts to fetch a URL with retries.

    Args:
        client: The httpx.AsyncClient instance.
        url (str): The URL to fetch.
        retries (int): Maximum number of retries.
        delay (int): Delay between retries in seconds.

    Returns:
        An httpx.Response object on success.

    Raises:
        httpx.HTTPError: When the maximum number of retries is exceeded.
    """
    for attempt in range(retries):
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response
        except (httpx.RequestError, httpx.HTTPStatusError, httpx.TimeoutException) as e:
            if attempt == retries - 1:
                return None
            await asyncio.sleep(delay)
