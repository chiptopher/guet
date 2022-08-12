import path from 'path';

import { Config } from '../config';
import { log } from '../native-wrapper';
import { configPath, getGitPath, readJSONFile, wrtiteJsonFile } from '../utils';

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

    const projectConfigPath = path.join(getGitPath(), 'repo.guetrc.json');
    const projectConfig = readJSONFile(projectConfigPath);
    projectConfig.currentCommittersInitials = args;
    wrtiteJsonFile(projectConfigPath, projectConfig);
}
