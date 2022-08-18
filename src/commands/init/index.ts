import { writeFileSync } from 'fs';
import path from 'path';

import { Initialize } from '../../chain-links/initialize';
import { MustHaveGit } from '../../chain-links/must-have-git';
import { ClosureChainLink, Command } from '../../command';
import { emptyConfig, emptyRepoInfo } from '../../config';
import { Args, getGitPath, wrtiteJsonFile } from '../../utils';
import { HooksCheck } from './hooks-check';
import { LocalPresent } from './local-preset';
import { createGitHookContent } from './util';

function init(args: Args) {
    wrtiteJsonFile(
        path.join(getGitPath(), 'repo.guetrc.json'),
        emptyRepoInfo()
    );
    maybeAddLocal(args);
    maybeAddHooks(args);
    console.log('guet successfully started in this repository.'.green);
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

function maybeAddLocal(args: string[]) {
    if (args.includes('--local')) {
        wrtiteJsonFile(path.join(process.cwd(), 'guetrc.json'), emptyConfig());
    }
}

export const initCommand = new Command(
    'init',
    { description: '', usage: '' },
    new Initialize()
        .next(new MustHaveGit('git not installed in this directory.'))
        .next(new LocalPresent())
        .next(new HooksCheck())
        .next(new ClosureChainLink(init))
);
