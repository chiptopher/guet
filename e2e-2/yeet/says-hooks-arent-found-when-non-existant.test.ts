import colors from 'colors';

import { assembleOutput, run } from '../utils';
colors.enable();
test('"guet yeet" removes the appropriate files when given flags', () => {
    run('git init');
    run('guet init');
    const [yeetNoFlags] = run('guet yeet');

    expect(yeetNoFlags).toEqual(
        assembleOutput([
            'Removed /test/.git/repo.guetrc.json'.green,
            'Not found /test/.git/hooks/pre-commit'.yellow,
            'Not found /test/.git/hooks/commit-msg'.yellow,
            'Not found /test/.git/hooks/post-commit'.yellow,
        ])
    );
});
