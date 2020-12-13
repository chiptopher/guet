import { Check } from './check';
import { Args } from '../../args';
import { filesystem } from 'gluegun';

export class GitRequiredCheck extends Check {
    constructor() {
        super('No git directory in this folder.');
    }

    public shouldStop(args: Args): boolean {
        return (
            filesystem.exists(filesystem.path(filesystem.cwd(), '.git')) && true
        );
    }
}
