import { execSync } from 'child_process';

import { Committer } from './committer';

export function setGitAuthor(committer: Committer) {
    execSync(`git config --local user.name "${committer.fullName}"`);
    execSync(`git config --local user.email ${committer.email}`);
}
