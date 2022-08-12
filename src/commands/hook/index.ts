import { readFileSync, writeFileSync } from 'fs';
import path from 'path';

import { getCurrentCommitters, setCurrentCommitters } from '../../committer';
import { COMMIT_EDITMSG, getGitPath } from '../../utils';
import { appendCoAuthoredBy, shuffleCommitters } from './util';

export function hook(args: string[]) {
    const [hookName] = args;
    switch (hookName) {
        case 'commit-msg':
            return commitMsg();
        case 'post-commit':
            console.log('Running post-commit hook');
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
