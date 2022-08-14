import { run } from '../utils';

test('can get all the set committters', () => {
    run('git init');
    run('guet init');
    run('guet add f first first@example.com');
    run('guet add s second second@example.com');
    run('guet add t third third@example.com');
    run('guet set f s');
    const [output] = run('guet get current');
    expect(output).toEqual(
        'Current committers:\nf - first <first@example.com>\ns - second <second@example.com>\n'
    );
    const [output2] = run('guet get all');
    expect(output2).toEqual(
        'All committers:\nf - first <first@example.com>\ns - second <second@example.com>\nt - third <third@example.com>\n'
    );
});
