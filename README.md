# guet

> enable contribution tracking when pair programming with guet

Pair programming is integral part of many software development lifecycles. When pairing, you may want to track each committer's contributions. Using **guet** enables that functionality without changing the normal git workflow.


## Install

To include it in your project:
```
npm install guet -D
```

To install globally:
```
npm install -g guet
```

## Usage
Below are the available commands. For more detailed usage documentation, run `guet <command> --help`.

| Command | Description |
| ------------ | ---------------------------------|
| init  | start using guet in the current repository |
| add | add committers for use in pairing |
| set | set the current committers in the current repository
| get | get information about guet committers |
| remove | remove a committer by its initials |
| yeet | remove guet configurations |
| hook | apply guet modifications to the current git commit |

### In pre-existing hooks.

guet can easily integrate with other hook managing systems. In each of `pre-commit`, `commit-msg`, and `post-commit` within `.git/hooks/` you'll want to add each of the following commands respectively

```
// .git/hooks/pre-commit
npx guet hook pre-commit

// .git/hooks/commit-msg
npx guet hook commit-msg

// .git/hooks/post-commit
npx guet hook post-commit
```
