# guet
> enable contribution tracking when pair programming with guet

Pair programming is integral part of many software development lifecycles. When pairing, you may want to track both
pairs contributions. Using **guet** allows for that functionality.

[![Build Status](https://travis-ci.org/chiptopher/guet.svg?branch=master)](https://travis-ci.org/chiptopher/guet)

## Installation
**guet** can be installed from [pypi](https://pypi.org/project/guet/):

```
pip3 install guet
```

#### Development Version
The most recent develoment version can be downloaded and installed as well:

```
git clone https://github.com/chiptopher/guet.git
python setup.py install
```


## Usage

#### Initialization
`guet init` will initiailze the **guet** config files for the system.

#### Start
`guet start` will start **guet** for the reposotry at the current directory.
 
#### Resgister Committers
`guet add <initials> <"Name"> <email>` will register an available committer with the given initials, name and email.

#### Set Committers
`guet set [<initials>, ...]` will register the committers with the given initials to have their names attached to all
following commits.

## Contribution

Guidelines for contributions can be found [here](./docs/CONTRIBUTING.md). Feel free to 
[open an issue](https://github.com/chiptopher/guet/issues) if there are problems with **guet** or you want to submit a
feature request.
