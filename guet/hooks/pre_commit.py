from guet.config.most_recent_committers_set import most_recent_committers_set
from guet.currentmillis import current_millis


def pre_commit():
    now = current_millis()
    twenty_four_hours = 86400000
    twenty_four_hours_ago = now - twenty_four_hours
    set_time = most_recent_committers_set()
    if set_time < twenty_four_hours_ago:
        print("\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n")
        exit(1)
    else:
        exit(0)

