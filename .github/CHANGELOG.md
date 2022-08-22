# Changelog

## 4.0.0
This was a complete rewrite of the application, changing it's implementation from being python based to nodejs based. As such, the steps for downloading and using it have completely changed. Most of the CLI has remained unchanged, but there are a few differences. This is, however, a breaking change. `guet` config files from previous versions will not work with this one.

To migrate from the python version to the new typescript version, you'll want to do the following steps:
1. **Uninstall guet.** That cammand chould be `pip3 uninstall guet`
2. **Remove previous git hooks.** If you were using the raw guet hooks, this should be as simple as removing `pre-commit`, `post-commit`, and `commit-msg` in `.git/hooks`. If you were using it with something like husky, you'll have to remove those files and commands from your other git hooks.
3. **Install new guet.** If you want it globally available, that'd be `npm install -g guet`.
4. **Update hooks.** If you want guet to generate your hooks, you'll use the `--withHooks` flags in `guet init`. Otherwise in your `pre-commit`, `post-commit`, and `commit-msg` hooks you'll want to add the following commands respectively
```
// .git/hooks/pre-commit
npx guet hook pre-commit

// .git/hooks/commit-msg
npx guet hook commit-msg

// .git/hooks/post-commit
npx guet hook post-commit
```

## 3.0.1
### Bugs Fixed
* Removed error where commit messages were being overwritten entirely by Co-Authored lines

## 3.0.0
### Added Functionality
* Added `guet yeet` for remove guet tracking from a repository / computer.
* Removed `guet start`, and absorb that functionality into `guet init`.
* Add --location flag to `guet init` to specify what directory the guet hooks should be saved to.
* Remove `guet config`

### Notes
* Repos using git tracing from before 3.0.0 will have to update thier hooks. This can be done with `guet init -o`.

## 2.4.6
### Bugs Fixed
* When cancelling a guet start, a message saying that the repository was successfully started will no longer appear.

## 2.4.5
### Added Functionality
* When starting tracking in a repository, if a hooks folder isn't present one is created

## 2.4.4
### Added Functionality
* When setting committers, a message will print the committers that have been set.
* When starting a repository, a confirmation message will print that tracking is started on the repository.
* When attempting to start tracking a repository that already has hooks, a clearer prompt will appear.


## 2.4.3
### Added Functionality
*  When creating guet hooks on a system that doesn't have `python3`, the hook will use `python` instead
### Bugs Fixed
* Paths were not being correctly parsed when checking if guet hooks were present in path, causing guet sets to fail saying guet hasn't started in a given repository even if they have.

## 2.4.2
### Bugs Fixed
* Adding a committer locally that exactly matches a global committer won't create them locally.

## 2.4.1
### Added Functionality
* Commands that depend on the project root (`guet add --local`, `guet set`, etc.) can now be ran from nested directories from the project root.
* Initials in all commands are no longer case-sensitive.

## 2.4.0
Adds the `--local` flag to the `guet add` command that creates a `.guet/committers` directory with the committers saved. This committer can now be committed as a part of the repository. This commiter takes precedence over a globally saved committer.

Adds an error message for attempting to `guet set` from a folder that doesn't have a `.git` directory, usually signifying that the user is not in the project's root directory.

## 2.3.6
Addresses a typo in `guet get --help` which misspelled the `committers` identifier as `comitters`.

When committing with only one committer, guet will not append the `Co-authored` line in a commit.


## 2.3.5
Addresses a few bugs. When running `guet --help` / `guet -h` you should get the help message instead of an error. Also, providing an invalid commend (`guet invalid`) will print an error message saying `invalid` isn't a command, and then include the help message.

When working with [husky](https://github.com/typicode/husky) you have to provide `.git/hooks/pre-commit-guet` as the hook command in the husky definition. However, when calling that command it wouldn't actually run the guet script. It should now _actually_ run.

## 2.3.4
Address a bug where initial `guet set` calls would not configure the first commit to use the set committer as the git author. Instead, the system author would be used. Now the first committer supplied to the `guet set` call is used as the commit author.

## 2.3.3
Address a bug where upgrading from <2.3 would cause the `committersset` file to get into a malformed state.

Blocks `guet set` in a repository where `guet set` hasn't been ran.

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
