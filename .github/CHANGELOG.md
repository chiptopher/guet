# Changelog

## 2.1.0

Version 2.1.0 included two major features. First, you can actually set `pairReset=false` and have it work with your commits. Second `guet get` was added as a command. You can run it with the `current` identidier to get the current committers, and with the `committers` identifier to list out all of the committers on the system. For example:
```
$ guet get committers
All committers
cb -- chris boyer <cboyer@example.com>
ep -- first last <flast@example.com>
```

Additionally, passing the -l flag to either command will print out just the initials of the committers

```
$ guet get committers
cb, ep
```

## 2.0.0

Version 2.0 incorporated an almost entire rewrite of the working of guet, but didn't introduce many new features. Part of the rewrite included modifying the configuration files. Before 2.0, sqlite was used to manage the current committer. This has all been removed, and instread now manages those features with plain text files.

While this is easier to work with, it does require an upgrade. In addition to running `pip3 install guet --upgrade` to upgrade the guet package, you will also have to remove `~/.guet` as well as removing the `pre-commit`, `post-commit`, and `commit-msg` from the `.git/hooks` folders from all your projects currently using guet. Re-running `guet init` to regenerate the `~/.guet` folder and `guet start` to regenerate the commit hooks. You should to now be upgraded to 2.0.

Measures were talken as a part of the 2.0 rewrite to make it so complicated upgrades will not be necessary in the future.

All the commands work the same as they did before. One new command was introduced -- `guet config` -- which will allow for configuration of certain features in the future. However, none are currently configurable.
