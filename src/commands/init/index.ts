import fs, { writeFileSync } from 'fs';
import { homedir } from 'os';
import path from 'path';

import { emptyConfig, emptyRepoInfo } from '../../config';
import {
    Args,
    getGitPath,
    hasGitInCwd,
    writeConfig,
    wrtiteJsonFile,
} from '../../utils';
import { createGitHookContent } from './util';

export function init(args: Args) {
    const configDir = path.join(homedir(), '.guetrc.json');
    if (!fs.existsSync(configDir)) {
        writeConfig(emptyConfig());
    }
    if (!hasGitInCwd()) {
        console.log('git not installed in this directory.'.red);
        process.exit(1);
    } else {
        wrtiteJsonFile(
            path.join(getGitPath(), 'repo.guetrc.json'),
            emptyRepoInfo()
        );
        maybeAddHooks(args);
        console.log('guet successfully started in this repository.'.green);
    }
}

function maybeAddHooks(args: Args) {
    if (args.includes('--withHooks')) {
        createHook('pre-commit');
        createHook('post-commit');
        createHook('commit-msg');
        console.log('Creating pre-commit, post-commit, and commit-msg hooks.');
    }
}

function createHook(name: string) {
    writeFileSync(
        path.join(getGitPath(), 'hooks', name),
        createGitHookContent(name),
        { mode: 0o0755 }
    );
}
