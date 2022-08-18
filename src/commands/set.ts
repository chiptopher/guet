import { DateTime } from 'luxon';

import { MustHaveGit } from '../chain-links/must-have-git';
import { ClosureChainLink, Command } from '../command';
import {
    Committer,
    getAvailableCommitters,
    setCurrentCommitters,
} from '../committer';
import { log } from '../native-wrapper';
import { readRepoConfig, repoConfigExists, writeRepoConfig } from '../utils';

export function setCommitters(args: string[]) {
    if (!repoConfigExists()) {
        log(
            'Must run "guet init" to set paired committers for this repo.',
            'error'
        );
        process.exit(1);
    }

    // TODO refactor to use util methods
    const missingInitials = args.filter(
        arg =>
            !getAvailableCommitters()
                .map(committer => committer.initials)
                .includes(arg)
    );

    if (missingInitials.length > 0) {
        missingInitials.forEach(initials =>
            log(`No committer exists with the initials "${initials}".`, 'error')
        );
        process.exit(1);
    }

    const committers: Committer[] = args
        .map(arg => {
            return getAvailableCommitters().find(
                committer => committer.initials === arg
            );
        })
        .filter(committer => committer !== undefined) as Committer[];

    writeRepoConfig({
        ...readRepoConfig(),
        setTime: DateTime.now().toISO(),
    });

    setCurrentCommitters(committers);
}

export const setComand = new Command(
    'set',
    {
        description: 'set the current committers for this repository',
        usage: `set the current committers for this repository, but longer`,
    },
    new MustHaveGit(
        'Must run "guet init" to set paired committers for this repo.'
    ).next(new ClosureChainLink(setCommitters))
);
