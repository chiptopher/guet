import { run } from '../utils';

test('should set the current committers initials in the project', () => {
    run('git init');
    run('guet init');
    run('guet add FN "first name" fn@example.com');
    run('guet add sn "second name" sn@example.com');
    run('cd test');
    const [, exitCode] = run('guet set fn sn', './e2e');
    expect(exitCode).toEqual(0);
    const [output] = run('guet get current');
    expect(output).toEqual(
        'Current committers:\nfn - first name <fn@example.com>\nsn - second name <sn@example.com>\n'
    );
});
