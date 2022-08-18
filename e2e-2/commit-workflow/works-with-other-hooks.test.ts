import { writeFileSync } from 'fs';
import { join } from 'path';

import { getGitPath } from '../../src/utils';
import { run } from '../utils';
test('guet workflow works with hooks other than the generated ones', () => {
    run('git init');
    run('guet init');
    run('guet add f first first@example.com');
    run('guet add s second second@example.com');
    run('guet set f s');

    writeFileSync(
        join(getGitPath(), 'hooks', 'post-commit'),
        `
#!/usr/bin/env sh
echo "test pre-commit"
npx guet hook pre-commit
echo "done"
`,

        { mode: 0o0755 }
    );
    writeFileSync(
        join(getGitPath(), 'hooks', 'commit-msg'),
        `
#!/usr/bin/env sh
echo "test commit-msg"
npx guet hook commit-msg
echo "done"
`,

        { mode: 0o0755 }
    );
    writeFileSync(
        join(getGitPath(), 'hooks', 'post-commit'),
        `
#!/usr/bin/env sh
echo "test post-commit"
npx guet hook post-commit
echo "done"
`,

        { mode: 0o0755 }
    );

    run('git add .');
    run('git commit -m "Initial commit"');

    const [output] = run('git log');

    const gitOutput = output.split('\n');

    expect(gitOutput[1]).toEqual('Author: first <first@example.com>');

    expect(output.split('\n')[6]).toEqual(
        '    Co-authored-by: second <second@example.com>'
    );
});
