import { removeCommitterWithInitials } from '../../committer';
import { readConfig, writeConfig } from '../../utils';

export function remove(args: string[]) {
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
    config.committers = removeCommitterWithInitials(
        initialsFormatted[0],
        config.committers
    );
    writeConfig(config);
}