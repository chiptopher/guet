import { writeFileSync } from 'fs';
import { join } from 'path';

import colors from 'colors';

import { getGitPath } from '../../src/utils';
import { assembleOutput, run } from '../utils';

colors.enable();

test('"guet yeet" removes the appropriate files when given flags', () => {
    run('git init');
    run('guet init');

    writeFileSync(
        join(getGitPath(), 'hooks', 'pre-commit'),
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

    const [yeetNoFlags] = run('guet yeet');

    expect(yeetNoFlags).toEqual(
        assembleOutput([
            'Removed /test/.git/repo.guetrc.json'.green,
            "Skipped because it's been modified or isn't a guet hook /test/.git/hooks/pre-commit"
                .yellow,
            "Skipped because it's been modified or isn't a guet hook /test/.git/hooks/commit-msg"
                .yellow,
            "Skipped because it's been modified or isn't a guet hook /test/.git/hooks/post-commit"
                .yellow,
        ])
    );
});
