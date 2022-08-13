import fs from 'fs';
import path from 'path';

import { createGitHookContent } from '../../src/commands/init/util';
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
        createGitHookContent('pre-commit')
    );

    expect(
        fs.existsSync(path.join(getGitPath(), 'hooks', 'commit-msg'))
    ).toEqual(true);
    const commitMsgContent = fs.readFileSync(
        path.join(getGitPath(), 'hooks', 'commit-msg')
    );
    expect(String(commitMsgContent)).toEqual(
        createGitHookContent('commit-msg')
    );

    expect(
        fs.existsSync(path.join(getGitPath(), 'hooks', 'post-commit'))
    ).toEqual(true);
    const postCommitContent = fs.readFileSync(
        path.join(getGitPath(), 'hooks', 'post-commit')
    );
    expect(String(postCommitContent)).toEqual(
        createGitHookContent('post-commit')
    );
});
