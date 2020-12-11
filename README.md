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

### Upgrading

The version of **guet** installed can be upgraded using the following command:

```
pip3 install guet --upgrade
```

To see the version releases, changes between them, and upgrade guides, check the [change log](./.github/CHANGELOG.md)

### Installing a Specific Version

Installing a specific version of guet can be done with the following comming:

```
pip3 install guet==1.0.0
```

#### Development Version

The most recent development version can be downloaded and installed as well:

```
git clone https://github.com/chiptopher/guet.git
python setup.py install
```

## Usage

For full usage details, using `guet` will print out all commands and a description of what they do. Some of the ones most basic to the workflow are:

#### Initialization

`guet init` will initiailze the **guet** config files for the system.

#### Start

`guet start` will start **guet** for the repository at the current directory.

#### Register Committers

`guet add <initials> <"Name"> <email>` will register an available committer with the given initials, name and email.

```
$ guet add cb "Chiptopher" chiptopher@chiptopher.com
$ guet add jh "Jim Halpert" jimothy@dm.com
$ guet add ds "Dwight Schrute" dwight@dm.com
```

#### Set Committers

`guet set [<initials>, ...]` will register the committers with the given initials to have their names attached to all
following commits.

```
$ guet set cb ds
Committers set to
cb - Chiptopher <chiptopher@chiptopher.com>
ds - Dwight Schrute <dwight@dm.com>
```

## Questions

There is a [Frequently asked questions](.github/FAQ.md) section with some commonly asked questions.

## Contribution

Guidelines for contributions can be found [here](./.github/CONTRIBUTING.md). Feel free to
[open an issue](https://github.com/chiptopher/guet/issues) if there are problems with **guet** and you want to submit a
feature request.
