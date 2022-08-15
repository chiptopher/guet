import { DateTime } from 'luxon';

import { ClosureChainLink, Command } from '../command';
import {
    Committer,
    getAvailableCommitters,
    setCurrentCommitters,
} from '../committer';
import { Config } from '../config';
import { log } from '../native-wrapper';
import {
    configPath,
    readJSONFile,
    readRepoConfig,
    writeRepoConfig,
} from '../utils';

export function setCommitters(args: string[]) {
    // TODO refactor to use util methods
    const missingInitials = args.filter(
        arg =>
            !readJSONFile<Config>(configPath)
                .committers.map(committer => committer.initials)
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
        long: `set the current committers for this repository, but longer`,
        short: 'set the current committers for this repository',
    },
    new ClosureChainLink(setCommitters)
);
