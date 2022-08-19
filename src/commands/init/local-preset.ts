import { ChainLink } from '../../chain-links';
import { log } from '../../native-wrapper';
import { localConfigExists } from '../../utils';

export class LocalPresent extends ChainLink {
    protected doExecute(_args: string[]): void {
        if (localConfigExists()) {
            log(
                'Cannot initialize local config if one is already present',
                'error'
            );
            process.exit(1);
        }
    }
}
