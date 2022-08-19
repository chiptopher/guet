import { existsSync } from 'fs';
import { join } from 'path';

import { ChainLink } from '../../chain-links';
import { log } from '../../native-wrapper';
import { getGitPath } from '../../utils';

export class HooksCheck extends ChainLink {
    protected doExecute(_args: string[]): void {
        if (_args.includes('--withHooks')) {
            const found = ['pre-commit', 'commit-msg', 'post-commit'].filter(
                name => {
                    return existsSync(join(getGitPath(), 'hooks', name));
                }
            );

            if (found.length > 0) {
                log(
                    `Could not create nooks because the following hooks already exist: ${found.join(
                        ', '
                    )}.`,
                    'error'
                );
                process.exit(1);
            }
        }
    }
}
