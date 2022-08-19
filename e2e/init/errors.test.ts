import colors from 'colors';

import { assembleOutput, run } from '../utils';

colors.enable();

test('errors when in invalid state', () => {
    run('rm -rf .git');
    const [out, exitCode] = run('guet init');
    const expectedOutput = assembleOutput([
        'git not installed in this directory.'.red,
    ]);

    expect(out).toEqual(expectedOutput);
    expect(exitCode).toEqual(1);
});
