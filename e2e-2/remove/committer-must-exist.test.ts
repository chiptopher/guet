import colors from 'colors';

import { assembleOutput, run } from '../utils';

colors.enable();

test("erros when committer doesn't exist", () => {
    run('git init');
    run('guet init');
    run('guet add f first first@example.com');
    // it should ignore the case
    const [output, exitCode] = run('guet remove s');
    expect(output).toEqual(
        assembleOutput([`No committer exists with initials "s".`.red])
    );
    expect(exitCode).toEqual(1);
});
