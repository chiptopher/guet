import path from 'path';

import { RepoInfo } from '../../src/config';
import { getGitPath, readJSONFile } from '../../src/utils';
import { run } from '../utils';

test('should set the current committers initials in the project', () => {
    run('git init');
    run('guet init');
    run('guet add fn "first name" fn@example.com');
    run('guet add sn "second name" sn@example.com');

    run('guet set fn sn');

    const found = readJSONFile<RepoInfo>(
        path.join(getGitPath(), 'repo.guetrc.json')
    );

    expect(found.currentCommittersInitials).toEqual(['fn', 'sn']);
    expect(found.setTime).not.toEqual('');

    const [nameOutput] = run('git config user.name');
    const [emailOutput] = run('git config user.email');

    expect(nameOutput).toEqual('first name\n');
    expect(emailOutput).toEqual('fn@example.com\n');
});
