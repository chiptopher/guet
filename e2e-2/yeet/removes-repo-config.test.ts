import colors from 'colors';

import { assembleOutput, run } from '../utils';

colors.enable();

test('"guet yeet" removes the appropriate files when given flags', () => {
    run('git init');
    run('guet init --withHooks');
    const [yeetNoFlags] = run('guet yeet');
    expect(yeetNoFlags).toEqual(
        assembleOutput([
            `Removed /test/.git/repo.guetrc.json`.green,
            'Removed /test/.git/hooks/pre-commit'.green,
            'Removed /test/.git/hooks/commit-msg'.green,
            'Removed /test/.git/hooks/post-commit'.green,
        ])
    );
});
