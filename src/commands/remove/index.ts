import { Initialize } from '../../chain-links/initialize';
import { ClosureChainLink, Command } from '../../command';
import { removeCommitterWithInitials } from '../../committer';
import { log } from '../../native-wrapper';
import { readConfig } from '../../utils';

function remove(args: string[]) {
    const config = readConfig();
    let invalidInitialsGiven = false;
    const initialsFormatted = args.map(arg => arg.toLowerCase());

    initialsFormatted
        .map(initials => initials.toLowerCase())
        .forEach(initials => {
            if (
                !config.committers.find(
                    committer => committer.initials === initials
                )
            ) {
                log(
                    `No committer exists with initials "${initials}".`,
                    'error'
                );
                invalidInitialsGiven = true;
            }
        });
    if (invalidInitialsGiven) {
        process.exit(1);
    }
    removeCommitterWithInitials(initialsFormatted[0]);
}

export const removeCommand = new Command(
    'remove',
    {
        description: 'remove a committer by its initials',
        usage: 'guet remove <initials>',
    },
    new Initialize().next(new ClosureChainLink(remove)),
    true
);
