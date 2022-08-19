import { run } from '../utils';

test('"guet get available" separates local can global committers', () => {
    run('git init');
    run('guet init --local');
    run('guet add f First first@example.com');
    run('guet add f First2 first2@example.com --local');

    const [output] = run('guet get all');
    expect(output).toEqual(
        'All committers:\nf - First <first@example.com> (overriden)\n\n(local)\nf - First2 <first2@example.com>\n'
    );
});
