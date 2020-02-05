# Changelog

## 2.3.2
Address a bug where each character in the stacktrace for the error message would print on a new line. Also include the path to the file containing stacktraces.

Now, trying to add a new committer with the same initials as an already present committers will prompt the user to confirm if they want to overwrite the committer.

## 2.3.1
Version 2.3.1 makes it so `guet set` cannot be ran in directories where there is no git repository present.

## 2.3.0
Version 2.3.0 introduces the ability to have multiple `guet set` configurations between repositories. A `guet set` in `ProjectA` and `ProjectB` can be ran without one affecting the other. Previously, if committers were set in `ProjectA`, they would be used in `ProjectB` as well. Currently set committers were shared project wide.

The `--version` flag was added to print the current guet version. 

## 2.2.0

Version 2.2.0 introduces a new command, `guet remove <initials>`, for removing a committer from the system.

Additionally, typing the `-a|--alongside` and `-o|--overwrite` flags were added to `guet start`. When starting guet in a
directory where there are already hooks. You're promped with the following message:
```
$ guet start
There is already commit hooks in this project. Would you like to overwrite (o),
create (a) the file and put it in the hooks folder, or cancel (x)?
```

Now, if you already know that you would like to overwrite the current hooks, `guet start -o` will do that. `guet start -a`
will automatically create the hooks appended with `-guet`. Both skip the prompt.

## 2.1.1

Version 2.1.1 introduces help messages for all the commands. For all commands, this can be invoked using `--help` and `-h` flags. Additionally, for all commands other than `init` and `start`, running `guet <command>` will also print the help message.

## 2.1.0

Version 2.1.0 included two major features. First, you can actually set `pairReset=false` and have it work with your commits. Second `guet get` was added as a command. You can run it with the `current` identidier to get the current committers, and with the `committers` identifier to list out all of the committers on the system. For example:
```
$ guet get committers
All committers
cb -- chris boyer <cboyer@example.com>
ep -- first last <flast@example.com>
```

Additionally, passing the `-l` flag to either command will print out just the initials of the committers

```
$ guet get committers -l
cb, ep
```

## 2.0.0

Version 2.0 incorporated an almost entire rewrite of the working of guet, but didn't introduce many new features. Part of the rewrite included modifying the configuration files. Before 2.0, sqlite was used to manage the current committer. This has all been removed, and instread now manages those features with plain text files.

While this is easier to work with, it does require an upgrade. In addition to running `pip3 install guet --upgrade` to upgrade the guet package, you will also have to remove `~/.guet` as well as removing the `pre-commit`, `post-commit`, and `commit-msg` from the `.git/hooks` folders from all your projects currently using guet. Re-running `guet init` to regenerate the `~/.guet` folder and `guet start` to regenerate the commit hooks. You should to now be upgraded to 2.0.

Measures were talken as a part of the 2.0 rewrite to make it so complicated upgrades will not be necessary in the future.

All the commands work the same as they did before. One new command was introduced -- `guet config` -- which will allow for configuration of certain features in the future. However, none are currently configurable.
