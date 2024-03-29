import { run } from '../utils';

test('committers are rotated after the commit', () => {
    run('git init');
    run('guet init --withHooks');

    run('guet add f first first@example.com');
    run('guet add s second second@example.com');

    run('guet set f s');

    run('git add .');
    run('git commit -m "Initial commit"');

    run('touch A');
    run('git add .');
    run('git commit -m "Second commit"');

    const [output] = run('git log');

    const gitOutput = output.split('\n');

    expect(gitOutput[1]).toEqual('Author: second <second@example.com>');
    expect(gitOutput[9]).toEqual('Author: first <first@example.com>');
    expect(gitOutput[14]).toEqual(
        '    Co-authored-by: second <second@example.com>'
    );
});
