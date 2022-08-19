import { run } from '../utils';

test('removes the committer with the given intitials', () => {
    run('git init');
    run('guet init');
    run('guet add f first first@example.com');
    // it should ignore the case
    run('guet remove F');
    const [output] = run('guet get all');

    expect(output).toEqual('All committers:\n');
});
