import { readFileSync } from 'fs';
import path from 'path';

import { getGitPath } from '../src/utils';
import { cleanup, run } from './utils';

describe('guet hook', () => {
    beforeEach(() => {
        cleanup();
    });

    describe('commit_msg', () => {
        it('should append the Co-authored-by message of the co-authors', () => {
            run('git init');
            run('guet init');
            run('guet add f1 "f1" f1@example.com');
            run('guet add f2 "f2" f2@example.com');
            run('guet set f1 f2');

            run('git add .');
            run('git commit -m "Initial commit"');

            run('guet hook commit_msg');

            const output = readFileSync(
                path.join(getGitPath(), 'COMMIT_EDITMSG')
            );

            expect(String(output)).toEqual(
                'Initial commit\n\nCo-authored-by: f2 <f2@example.com>'
            );
        });

        it('should append set no Co-authored-by if only one committer is set', () => {
            run('git init');
            run('guet init');
            run('guet add f1 "f1" f1@example.com');
            run('guet set f1');

            run('git add .');
            run('git commit -m "Initial commit"');

            run('guet hook commit_msg');

            const output = readFileSync(
                path.join(getGitPath(), 'COMMIT_EDITMSG')
            );

            expect(String(output)).toEqual('Initial commit\n\n');
        });

        it('should remove previous Co-authored-by if editing a commit', () => {
            run('git init');
            run('guet init');
            run('guet add f1 "f1" f1@example.com');
            run('guet add f2 "f2" f2@example.com');
            run('guet add f3 "f3" f3@example.com');
            run('guet add f4 "f4" f4@example.com');
            run('git add .');
            run('git commit -m "Initial commit"');

            run('guet set f1 f2');
            run('guet hook commit_msg');

            run('touch NEW_FILE');
            run('git add .');
            run('git commit --amend --no-edit');

            run('guet set f3 f4');
            run('guet hook commit_msg');

            const output = readFileSync(
                path.join(getGitPath(), 'COMMIT_EDITMSG')
            );

            expect(String(output)).toEqual(
                'Initial commit\n\nCo-authored-by: f4 <f4@example.com>'
            );
        });
    });
});
