import { run } from '../../ts-e2e/utils';

test('should append the co-authored messages for co-authors', () => {
    run('git init');
    run('guet init --withHooks');
    run('guet add f1 "f1" f1@example.com');
    run('guet add f2 "f2" f2@example.com');
    run('guet set f1 f2');

    run('git add .');
    run('git commit -m "Initial commit"');

    const [output] = run('git log');

    expect(output.split('\n')[6]).toEqual(
        '    Co-authored-by: f2 <f2@example.com>'
    );
});
