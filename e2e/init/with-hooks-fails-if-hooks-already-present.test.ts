import { writeFileSync } from 'fs';
import path from 'path';

import colors from 'colors';

import { getGitPath } from '../../src/utils';
import { assembleOutput, run } from '../utils';

colors.enable();

test('"guet init --withHooks" fails if there are already hooks in this folder', () => {
    run('git init');

    writeFileSync(
        path.join(getGitPath(), 'hooks', 'pre-commit'),
        '#! /usr/bin/env python3\n'
    );
    writeFileSync(
        path.join(getGitPath(), 'hooks', 'commit-msg'),
        '#! /usr/bin/env python3\n'
    );
    writeFileSync(
        path.join(getGitPath(), 'hooks', 'post-commit'),
        '#! /usr/bin/env python3\n'
    );

    const [output, exitCode] = run('guet init --withHooks');
    expect(exitCode).toEqual(1);
    expect(output).toEqual(
        assembleOutput([
            'Could not create nooks because the following hooks already exist: pre-commit, commit-msg, post-commit.'
                .red,
        ])
    );
});
