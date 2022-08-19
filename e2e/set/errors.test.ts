import colors from 'colors';

import { assembleOutput, run } from '../utils';

colors.enable();

test('should display error message when given unknown initials', () => {
    run('git init');
    run('guet init');
    run('guet add fn "first name" fn@example.com');
    const [out, errorCode] = run('guet set fn fn2');

    expect(out).toEqual(
        assembleOutput(['No committer exists with the initials "fn2".'.red])
    );

    expect(errorCode).toEqual(1);
});
