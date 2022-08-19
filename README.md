# guet

> enable contribution tracking when pair programming with guet

Pair programming is integral part of many software development lifecycles. When pairing, you may want to track each committer's contributions. Using **guet** enables that functionality without changing the normal git workflow.


## Install
```
npm install guet -D
```

## Usage

| Command | Description |
| ------------ | ---------------------------------|
| init  | start using guet in the current repository |
| add | add committers for use in pairing |
| set | set the current committers in the current repository
| get | get information about guet committers |
| remove | remove a committer by its initials |
| yeet | remove guet configurations |
| hook | apply guet modifications to the current git commit |
