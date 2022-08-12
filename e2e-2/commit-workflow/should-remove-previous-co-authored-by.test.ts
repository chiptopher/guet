import { run } from '../../ts-e2e/utils';

it('should remove previous Co-authored-by if editing a commit', () => {
    run('git init');
    run('guet init --withHooks');
    run('guet add f1 "f1" f1@example.com');
    run('guet add f2 "f2" f2@example.com');
    run('guet add f3 "f3" f3@example.com');
    run('guet add f4 "f4" f4@example.com');
    run('guet set f1 f2');

    run('git add .');
    run('git commit -m "Initial commit"');

    run('touch NEW_FILE');
    run('git add .');

    run('guet set f3 f4');
    run('git commit --amend --no-edit');

    const [output] = run('git log');

    expect(output.split('\n')[6]).toEqual(
        '    Co-authored-by: f4 <f4@example.com>'
    );
});
