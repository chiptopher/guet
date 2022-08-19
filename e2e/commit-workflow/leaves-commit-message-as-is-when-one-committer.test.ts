import { run } from '../utils';

test('should append set no Co-authored-by if only one committer is set', () => {
    run('git init');
    run('guet init --withHooks');
    run('guet add f1 "f1" f1@example.com');
    run('guet set f1');

    run('git add .');
    run('git commit -m "Initial commit"');
    const [output] = run('git log');

    expect(output.split('\n')).toHaveLength(6);
});
