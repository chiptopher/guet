import { run } from '../utils';

test('blocks commit when no committers are set', () => {
    run('git init');
    run('guet init --withHooks');
    run('git add .');
    const [, exitCode] = run('git commit -m "Initial commit"');
    expect(exitCode).toEqual(1);
    const [output] = run('git log');
    expect(output).toEqual(
        "fatal: your current branch 'main' does not have any commits yet\n"
    );
});
