import { ClosureChainLink, Command } from '../../command';
import { removeCommitterWithInitials } from '../../committer';
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
                console.log(
                    `No committer exists with initials "${initials}".`.red
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
        description: '',
        usage: '',
    },
    new ClosureChainLink(remove)
);
