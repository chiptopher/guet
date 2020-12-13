import { filesystem } from 'gluegun';
import { NoProjectRootError } from '../errors';

export function projectRoot() {
    let current = filesystem.cwd();
    while (current !== filesystem.homedir()) {
        if (filesystem.exists(filesystem.path(current, '.git'))) {
            return current;
        }
        current = filesystem.path(current, '..');
    }
    throw new NoProjectRootError();
}
