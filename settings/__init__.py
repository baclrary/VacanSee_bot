import os

from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

STAGE = os.getenv("STAGE", "dev")
TOKEN = os.getenv("TOKEN")

if STAGE == "dev":
    from .dev import *
elif STAGE == "prod":
    from .prod import *
else:
    raise ModuleNotFoundError(f"Couldn't find settings module for stage: {STAGE}")
