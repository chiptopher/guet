import { projectRoot } from '../util';
import { filesystem } from 'gluegun';

enum HookName {
    CommitMsg,
    PreCommit,
    PostCommit,
}

export function hooksPresent() {
    try {
        projectRoot();
    } catch (e) {
        return false;
    }
}

function gitDirectoryPath(): string {
    return filesystem.path(projectRoot(), '.git');
}
