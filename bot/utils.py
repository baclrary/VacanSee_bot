import asyncio
import json

import aiofiles
import httpx

from database.crud import create_user, get_user


async def get_user_translation(user_id):
    """
    Asynchronously retrieves translations for a given user's preferred language.

    Args:
        user_id: The unique identifier of the telegram user

    Returns:
        A dictionary containing the translations for the user's preferred language.

    Raises:
        FileNotFoundError: If the translations file for the user's language does not exist.
        ValueError: If the translations file is not a valid JSON file.
        Exception: For any unexpected errors during the operation.
    """
    try:
        user = await get_user(user_id)
        user_language = user.lang

        translations_path = f"bot/langs/{user_language}.json"
        async with aiofiles.open(translations_path, "r", encoding="utf-8") as file:
            translations = await file.read()
            return json.loads(translations)

    except FileNotFoundError:
        raise FileNotFoundError(f"Language file for {user_language} not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {translations_path}.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}.")


async def ensure_user_exists(user_id: int):
    """
    Retrieves an existing user from the database or creates a new one with default settings.

    Args:
        user_id (int): The ID of the user.

    Returns:
        The user object.
    """
    user = await get_user(user_id)
    if not user:
        user = await create_user(id=user_id, lang="eng", is_premium=False)
    return user


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
