import traceback

from guet.config.set_errors import set_errors


def log_on_error(f):
    def wrapper():
        try:
            f()
        except Exception:
            print('An error has occurred, please refer to error logs for more information\n')
            stack_tract = traceback.format_exc()
            set_errors(stack_tract)

    return wrapper
