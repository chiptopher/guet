import colors from 'colors';

import { assembleOutput, run } from '../utils';

colors.enable();

test('it should allow you to create an overlapping user without --force when using --local', () => {
    run('git init');
    run('guet init --local');
    run('guet add f First first@example.com');
    const [output] = run('guet add f First2 first2@example.com --local');
    expect(output).toEqual(
        assembleOutput([
            `Added committer will be used over global committer with initials "f" in this repository.`
                .yellow,
        ])
    );
});
