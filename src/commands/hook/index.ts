import { readFileSync, writeFileSync } from 'fs';
import path from 'path';

import { DateTime } from 'luxon';

import { ClosureChainLink, Command } from '../../command';
import { getCurrentCommitters, setCurrentCommitters } from '../../committer';
import { COMMIT_EDITMSG, getGitPath, readRepoConfig } from '../../utils';
import {
    appendCoAuthoredBy,
    shouldResetCommitters,
    shuffleCommitters,
} from './util';

function hook(args: string[]) {
    const [hookName] = args;
    switch (hookName) {
        case 'pre-commit':
            return preCommit();
        case 'commit-msg':
            return commitMsg();
        case 'post-commit':
            return postCommit();
    }
}

function commitMsg() {
    const committers = getCurrentCommitters();

    const [_, ...followingCommitters] = committers;
    const commitMsgPath = path.join(getGitPath(), COMMIT_EDITMSG);
    const currentMessage = String(readFileSync(commitMsgPath));
    writeFileSync(
        commitMsgPath,
        appendCoAuthoredBy(currentMessage, followingCommitters)
    );
}

function postCommit() {
    setCurrentCommitters(shuffleCommitters(getCurrentCommitters()));
}

function preCommit() {
    if (getCurrentCommitters().length === 0) {
        console.log('No committers set.'.red);
        process.exit(1);
    }
    if (
        shouldResetCommitters(
            DateTime.now(),
            DateTime.fromISO(readRepoConfig().setTime)
        )
    ) {
        console.log(
            'Committers last let over 24 hours ago. Please reset them.'.red
        );
        process.exit(1);
    }
}

export const hookCommand = new Command(
    'hook',
    { description: '', usage: '' },
    new ClosureChainLink(hook)
);
