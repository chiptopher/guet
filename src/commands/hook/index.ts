import { readFileSync, writeFileSync } from 'fs';
import path from 'path';

import { getCurrentCommitters } from '../../committer';
import { COMMIT_EDITMSG, getGitPath } from '../../utils';
import { appendCoAuthoredBy } from './util';

export function hook(args: string[]) {
    const [hookName] = args;
    switch (hookName) {
        case 'commit-msg':
            commitMsg();
            break;
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
