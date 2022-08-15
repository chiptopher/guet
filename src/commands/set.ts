import { DateTime } from 'luxon';

import { getAvailableCommitters } from '../committer';
import { Config } from '../config';
import { setGitAuthor } from '../git';
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

    const projectConfig = readRepoConfig();
    projectConfig.setTime = DateTime.now().toISO();
    projectConfig.currentCommittersInitials = args;
    writeRepoConfig(projectConfig);

    const author = getAvailableCommitters().find(
        committer => committer.initials === args[0]
    );

    if (author) {
        setGitAuthor(author);
    }
}
