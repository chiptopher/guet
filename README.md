# guet

> enable contribution tracking when pair programming with guet

Pair programming is integral part of many software development lifecycles. When pairing, you may want to track each committer's contributions. Using **guet** enables that functionality without changing the normal git workflow.

[![Actions Status](https://github.com/chiptopher/guet/workflows/guetci/badge.svg)](https://github.com/chiptopher/guet/workflows/guetci/badge.svg)
[![PyPI version](https://badge.fury.io/py/guet.svg)](https://badge.fury.io/py/guet)
![PyPI - Downloads](https://img.shields.io/pypi/dm/guet)

## Installation

**guet** can be installed from [pypi](https://pypi.org/project/guet/):

```
pip3 install guet
```

## Usage

### init

Initialize repository for guet tracking.

```
$ guet init
```

| Flag                        | Description                          |
| --------------------------- | ------------------------------------ |
| --location [path to foler]  | Specify directory to create hooks in |
| --alongside / -a            | Append -guet to hook file names      |
| --overwrite / -o            | Overwrite existing hooks             |


### add

Add a committer for commit tracking

```
$ guet add p1 "Person 1" person@example.com
```

| Flag                        | Description                           |
| --------------------------- | ------------------------------------  |
| --local                     | Add users locally to this repository (and create local configuration files |


### set

Set committers for current repository

```
$ guet set p1 p2
Committers set to:
p1 - Person 1 <person1@example.com>
p2 - Person 2 <person2@example.com>
```

### get

Get committers.

```
$ guet get all
All committers
p1 - Person 1 <person1@example.com>
p2 - Person 2 <person2@example.com>
p3 - Person 2 <person2@example.com>

$ guet get current
Current committers
p1 - Person 1 <person1@example.com>
p3 - Person 2 <person2@example.com>
```

### remove

Remove committer

```
$ guet remove p1
```

### yeet

Remove guet configurations.

```
$ guet yeet
```

| Flag                        | Description                           |
| --------------------------- | ------------------------------------  |
| --global / -g               | Remove guet configuration from home directory


## Questions

There is a [frequently asked questions](.github/FAQ.md) section with some commonly asked questions.

## Contribution

Guidelines for contributions can be found [here](./.github/CONTRIBUTING.md). Feel free to
[open an issue](https://github.com/chiptopher/guet/issues) if there are problems with **guet** or you want to submit a
feature request.
