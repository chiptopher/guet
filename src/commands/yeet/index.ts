import fs, { existsSync } from 'fs';
import path from 'path';

import { Initialize } from '../../chain-links/initialize';
import { MustHaveGit } from '../../chain-links/must-have-git';
import { ClosureChainLink, Command } from '../../command';
import { log } from '../../native-wrapper';
import { getGitPath } from '../../utils';
import { YeetHooks } from './hooks';

export const yeetCommand = new Command(
    'yeet',
    { description: '', usage: '' },
    new Initialize()
        .next(
            new MustHaveGit(
                'No files to remove because guet is not tracking this project.'
            )
        )
        .next(
            new ClosureChainLink(() => {
                const removeFilePathRelativeToGit = (url: string) => {
                    const found = path.resolve(path.join(getGitPath(), url));
                    if (existsSync(found)) {
                        fs.rmSync(found);
                        log(`Removed ${found}`, 'success');
                    } else {
                        log(`Not found ${found}`, 'warn');
                    }
                };
                removeFilePathRelativeToGit('repo.guetrc.json');
            }).next(new YeetHooks())
        )
);
