import { run } from '../utils';

test('should append the co-authored messages for co-authors, maintaining set order', () => {
    run('git init');
    run('guet init --local');
    run('guet add f first first@example.com');
    run('guet add s second second@example.com --local');
    run('guet add t third third@example.com');
    run('guet set f s');
    const [output] = run('guet get current');
    expect(output).toEqual(
        'Current committers:\nf - first <first@example.com>\ns - second <second@example.com>\n'
    );
});
