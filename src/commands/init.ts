import fs from 'fs';
import { homedir } from 'os';
import path from 'path';

import { emptyConfig, emptyRepoInfo } from '../config';
import { getGitPath, hasGitInCwd, writeConfig, wrtiteJsonFile } from '../utils';

export function init(_args: string[]) {
    const configDir = path.join(homedir(), '.guetrc.json');
    if (!fs.existsSync(configDir)) {
        writeConfig(emptyConfig());
    }
    if (!hasGitInCwd()) {
        console.log('git not installed in this directory.'.red);
    } else {
        wrtiteJsonFile(
            path.join(getGitPath(), 'repo.guetrc.json'),
            emptyRepoInfo()
        );
        console.log('guet successfully started in this repository.'.green);
    }
}
