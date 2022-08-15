import { separateFlags } from '../args';
import { ArgCount } from '../chain-links/arg-count';
import { ClosureChainLink, Command } from '../command';
import { Committer, removeCommitterWithInitials } from '../committer';
import { log } from '../native-wrapper';
import { readConfig, writeConfig } from '../utils';

export function add(args: string[]) {
    const [actualArgs, flags] = separateFlags(args);
    const [givenInitials, fullName, email] = actualArgs;
    const initials = givenInitials.toLowerCase();

    const config = readConfig();

    const found = config.committers.find(
        committer => committer.initials === initials
    );

    if (found) {
        if (flags.includes('--force')) {
            config.committers = removeCommitterWithInitials(
                initials,
                config.committers
            );
            log(
                `Overwritting previous committer with initials "${found.initials}".`
            );
        } else {
            log(
                `Failed to write "${initials}" "${fullName}" "${email}" because it would overwrite already present committer: "${found.initials}" "${found.fullName}" "${found.email}"`,
                'error'
            );
            log(
                'You can force this overwrite by adding the --force flag.',
                'error'
            );

            process.exit(1);
        }
    }

    const committer: Committer = {
        email,
        fullName,
        initials,
    };

    config.committers.push(committer);
    writeConfig(config);
}

export const addCommand = new Command(
    'add',
    {
        description: 'Add committers for use on commits.',
        usage: '',
    },
    new ArgCount(3, 3).next(new ClosureChainLink(add))
);
