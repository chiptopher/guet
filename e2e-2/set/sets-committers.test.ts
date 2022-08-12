import path from 'path';

import { RepoInfo } from '../../src/config';
import { getGitPath, readJSONFile } from '../../src/utils';
import { run } from '../../ts-e2e/utils';

test('should set the current committers initials in the project', () => {
    run('git init');
    run('guet init');
    run('guet add fn "first name" fn@example.com');
    run('guet add sn "second name" sn@example.com');

    run('guet set fn sn');

    const found = readJSONFile<RepoInfo>(
        path.join(getGitPath(), 'repo.guetrc.json')
    );

    expect(found).toEqual({
        currentCommittersInitials: ['fn', 'sn'],
    });
});
