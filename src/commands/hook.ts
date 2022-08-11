import { readFileSync, writeFileSync } from 'fs';
import path from 'path';

import { getCurrentCommitters } from '../committer';
import { COMMIT_EDITMSG, getGitPath } from '../utils';

export function hook(args: string[]) {
    const [hookName] = args;
    switch (hookName) {
        case 'commit_msg':
            commitMsg();
            break;
    }
}

function commitMsg() {
    const committers = getCurrentCommitters();

    const [_, ...followingCommitters] = committers;
    const coAuthoredLines = followingCommitters
        .map(
            committer =>
                `Co-authored-by: ${committer.fullName} <${committer.email}>`
        )
        .join('\n');
    const commitMsgPath = path.join(getGitPath(), COMMIT_EDITMSG);
    const currentMessage = readFileSync(commitMsgPath);
    writeFileSync(commitMsgPath, currentMessage + '\n' + coAuthoredLines);
}
