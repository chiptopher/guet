import { ChainLink } from '../../chain-links';
import { log } from '../../native-wrapper';
import { repoConfigExists } from '../../utils';

export class RepoConfigPreset extends ChainLink {
    protected doExecute(_args: string[]): void {
        if (repoConfigExists()) {
            log('guet already initialized in this repository.', 'error');
            process.exit(1);
        }
    }
}
