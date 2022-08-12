import fs from 'fs';
import path from 'path';

import { getGitPath } from '../../src/utils';
import { run } from '../utils';

test('creates pre-commit, commiit-msg, and post-commit files that have appropriate content', () => {
    run('git init');
    run('guet init --withHooks');
    expect(
        fs.existsSync(path.join(getGitPath(), 'hooks', 'pre-commit'))
    ).toEqual(true);
    const preCommitContent = fs.readFileSync(
        path.join(getGitPath(), 'hooks', 'pre-commit')
    );
    expect(String(preCommitContent)).toEqual(
        '#!/usr/bin/env sh\nnpx guet hook pre-commit\n'
    );

    expect(
        fs.existsSync(path.join(getGitPath(), 'hooks', 'commit-msg'))
    ).toEqual(true);
    const commitMsgContent = fs.readFileSync(
        path.join(getGitPath(), 'hooks', 'commit-msg')
    );
    expect(String(commitMsgContent)).toEqual(
        '#!/usr/bin/env sh\nnpx guet hook commit-msg\n'
    );

    expect(
        fs.existsSync(path.join(getGitPath(), 'hooks', 'post-commit'))
    ).toEqual(true);
    const postCommitContent = fs.readFileSync(
        path.join(getGitPath(), 'hooks', 'post-commit')
    );
    expect(String(postCommitContent)).toEqual(
        '#!/usr/bin/env sh\nnpx guet hook post-commit\n'
    );
});
