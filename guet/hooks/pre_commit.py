from guet.config.errors import PairSetError
from guet.config.get_config import get_config
from guet.config.get_current_committers import get_current_committers
from guet.config.most_recent_committers_set import most_recent_committers_set
from guet.currentmillis import current_millis
from guet.util.errors import log_on_error


@log_on_error
def pre_commit():
    settings = get_config()
    if len(get_current_committers()) == 0:
        _fail_because_there_are_no_current_committers()
    elif settings.read('pairReset'):
        _fail_if_past_valid_timeframe()


def _fail_because_there_are_no_current_committers():
    print('You must set your pairs before you can commit.\n')
    exit(1)


def _fail_if_past_valid_timeframe():
    now = current_millis()
    twenty_four_hours = 86400000
    twenty_four_hours_ago = now - twenty_four_hours
    try:
        set_time = most_recent_committers_set()
        if set_time < twenty_four_hours_ago:
            print(("\nYou have not reset pairs in over twenty four hours!\n" +
                   "Please reset your pairs by using guet set and including your pairs' initials\n"))
            exit(1)
    except PairSetError:
        _fail_because_there_are_no_current_committers()
