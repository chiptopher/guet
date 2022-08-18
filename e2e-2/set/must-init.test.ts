import colors from 'colors';

import { assembleOutput, run } from '../utils';

colors.enable();

test("errors when the project doesn't have an init run", () => {
    run('guet add f first first@example.com');
    run('guet add s second second@example.com');
    const [withoutGit, exitCode] = run('guet set f s');
    const expectedOutput = assembleOutput([
        'Must run "guet init" to set paired committers for this repo.'.red,
    ]);
    expect(withoutGit).toEqual(expectedOutput);
    expect(exitCode).toEqual(1);
    run('git init');
    const [withoutInit, withoutInitExitCode] = run('guet set f s');
    expect(withoutInit).toEqual(withoutInit);
    expect(withoutInitExitCode).toEqual(1);
});
