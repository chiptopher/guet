import colors from 'colors';

import { assembleOutput, run } from '../utils';

colors.enable();

test('--withLocal flag fails when one already present', () => {
    run('git init');
    run('guet init --local');
    const [output, exitCode] = run('guet init --local');

    expect(exitCode).toEqual(1);
    expect(output).toEqual(
        assembleOutput([
            'Cannot initialize local config if one is already present'.red,
        ])
    );
});
