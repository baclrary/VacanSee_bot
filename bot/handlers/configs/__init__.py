from .create_config import create_config_conv_handler
from .delete_all_configs import (
    ask_delete_all_configs_confirmation_handler,
    cancel_delete_all_configs_handler,
    confirm_delete_all_configs_handler,
)
from .delete_config import (
    ask_delete_config_confirmation_handler,
    cancel_delete_config_handler,
    confirm_delete_config_handler,
)
from .display_configs import display_configs_handler
from .edit_config import edit_config_conv_handler
from .get_config import get_config_handler

all_configs_handlers = [
    create_config_conv_handler,
    ask_delete_all_configs_confirmation_handler,
    cancel_delete_all_configs_handler,
    confirm_delete_all_configs_handler,
    ask_delete_config_confirmation_handler,
    cancel_delete_config_handler,
    confirm_delete_config_handler,
    display_configs_handler,
    get_config_handler,
    edit_config_conv_handler,
]
