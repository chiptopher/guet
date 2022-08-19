import { run } from '../utils';

test('should append the co-authored messages for co-authors, maintaining set order', () => {
    run('git init');
    run('guet init --withHooks --local');
    run('guet add f1 "f1" f1@example.com --local');
    run('guet add f2 "f2" f2@example.com');
    run('guet set f2 f1');

    run('git add .');
    run('git commit -m "Initial commit"');

    const [output] = run('git log');

    expect(output.split('\n')[6]).toEqual(
        '    Co-authored-by: f1 <f1@example.com>'
    );
});
