import colors from 'colors';

import { assembleOutput, run } from '../utils';

colors.enable();

test('"guet add --local" will fail if "guet init --local" hasn\'t been ran in the folder', () => {
    run('git init');
    const [output, exitCode] = run(
        'guet add f First first@example.com --local'
    );
    expect(exitCode).toEqual(1);
    expect(output).toEqual(
        assembleOutput([
            'guet not initialized in this repository. Run "guet init --local" to start local tracking in this repository.'
                .red,
        ])
    );
});
