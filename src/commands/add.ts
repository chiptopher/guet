import { separateFlags } from '../args';
import { ArgCount } from '../chain-links/arg-count';
import { Initialize } from '../chain-links/initialize';
import { ClosureChainLink, Command } from '../command';
import {
    addCommitter,
    Committer,
    removeCommitterWithInitials,
} from '../committer';
import { log } from '../native-wrapper';
import { localConfigExists, readConfig } from '../utils';

export function add(args: string[]) {
    const [actualArgs, flags] = separateFlags(args);
    const [givenInitials, fullName, email] = actualArgs;
    const initials = givenInitials.toLowerCase();

    if (flags.includes('--local') && !localConfigExists()) {
        log(
            'guet not initialized in this repository. Run "guet init --local" to start local tracking in this repository.',
            'error'
        );
        process.exit(1);
    }

    const globalConfig = readConfig();

    const found = globalConfig.committers.find(
        committer => committer.initials === initials
    );

    if (found) {
        if (flags.includes('--force')) {
            removeCommitterWithInitials(initials);
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

    addCommitter(committer, flags.includes('--local') ? 'local' : 'global');
}

export const addCommand = new Command(
    'add',
    {
        description: 'Add committers for use on commits.',
        usage: '',
    },
    new Initialize().next(new ArgCount(3, 3)).next(new ClosureChainLink(add))
);
