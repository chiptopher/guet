import { assembleOutput, run } from '../utils';

test("errors when the project doesn't have an init run", () => {
    run('git init');
    run('guet add f first first@example.com');
    run('guet add s second second@example.com');
    const [output, exitCode] = run('guet set f s');
    expect(output).toEqual(
        assembleOutput([
            'Must run "guet init" to set paired committers for this repo.'.red,
        ])
    );

    expect(exitCode).toEqual(1);
});
