import fs from 'fs';
import { homedir } from 'os';
import path from 'path';

import { emptyConfig } from '../config';
import { hasGitInCwd } from '../utils';

export function init(_args: string[]) {
    const configDir = path.join(homedir(), '.guetrc.json');
    if (!fs.existsSync(configDir)) {
        fs.writeFileSync(configDir, JSON.stringify(emptyConfig()));
    }
    if (!hasGitInCwd()) {
        console.log('git not installed in this directory.'.red);
    } else {
        console.log('guet successfully started in this repository.'.green);
    }
}
