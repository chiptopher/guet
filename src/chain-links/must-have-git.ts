import { ChainLink } from '.';
import { log } from '../native-wrapper';
import { getProjectAbsolutePath } from '../utils';

export class MustHaveGit extends ChainLink {
    private errorMessage: string;
    constructor(errorMessage: string) {
        super();
        this.errorMessage = errorMessage;
    }

    protected doExecute(_args: string[]): void {
        const result = getProjectAbsolutePath();
        if (!result) {
            log(this.errorMessage, 'error');
            process.exit(1);
        }
    }
}
