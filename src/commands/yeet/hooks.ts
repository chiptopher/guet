import fs, { existsSync, readFileSync } from 'fs';
import path from 'path';

import { ChainLink } from '../../chain-links';
import { log } from '../../native-wrapper';
import { getGitPath } from '../../utils';
import { createGitHookContent } from '../init/util';

export class YeetHooks extends ChainLink {
    protected doExecute(_args: string[]): void {
        ['pre-commit', 'commit-msg', 'post-commit'].forEach(hookName => {
            const finalPath = path.resolve(
                path.join(getGitPath(), 'hooks', hookName)
            );
            if (!existsSync(finalPath)) {
                log(`Not found ${finalPath}`, 'warn');
            } else {
                if (
                    String(readFileSync(finalPath)) !==
                    createGitHookContent(hookName)
                ) {
                    log(
                        `Skipped because it's been modified or isn't a guet hook ${finalPath}`,
                        'warn'
                    );
                } else {
                    fs.rmSync(finalPath);
                    log(`Removed ${finalPath}`, 'success');
                }
            }
        });
    }
}
