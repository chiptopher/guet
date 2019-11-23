import traceback

from guet.config.set_errors import set_errors


def log_on_error(wrapped):
    def wrapper():
        try:
            wrapped()
        # pylint: disable=broad-except
        except Exception:
            print('An error has occurred, please refer to error logs for more information\n')
            stack_tract = traceback.format_exc()
            set_errors(stack_tract)
            exit(1)

    return wrapper
