import path from 'path';

import colors from 'colors';

import { RepoInfo } from '../src/config';
import { getGitPath, readJSONFile } from '../src/utils';
import { assembleOutput, run } from './utils';

colors.enable();

describe('guet set', () => {
    it('should display error message when given unknown initials', () => {
        run('git init');
        run('guet init');
        run('guet add fn "first name" fn@example.com');
        const [out, errorCode] = run('guet set fn fn2');

        expect(out).toEqual(
            assembleOutput(['No committer exists with the initials "fn2".'.red])
        );

        expect(errorCode).toEqual(1);
    });

    it('should set the current committers initials in the project', () => {
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
});
