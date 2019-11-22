# Changelog

## 2.0.0

Version 2.0 incorporated an almost entire rewrite of the working of guet, but didn't introduce many new features. Part of the rewrite included modifying the configuration files. Before 2.0, sqlite was used to manage the current committer. This has all been removed, and instread now manages those features with plain text files.

While this is easier to work with, it does require an upgrade. In addition to running `pip3 install guet --upgrade` to upgrade the guet package, you will also have to remove `~/.guet` as well as removing the `pre-commit`, `post-commit`, and `commit-msg` from the `.git/hooks` folders from all your projects currently using guet. Re-running `guet init` to regenerate the `~/.guet` folder and `guet start` to regenerate the commit hooks. You should to now be upgraded to 2.0.

Measures were talken as a part of the 2.0 rewrite to make it so complicated upgrades will not be necessary in the future.

All the commands work the same as they did before. One new command was introduced -- `guet config` -- which will allow for configuration of certain features in the future. However, none are currently configurable.
