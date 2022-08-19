import path from 'path';

import { readJSONFile } from '../../src/utils';
import { run } from '../utils';

test('Including --local when creating a committer adds it to the local config file', () => {
    run('git init');
    run('guet init --local');
    const [, exitCode] = run('guet add f first first@example.com --local');
    expect(exitCode).toEqual(0);

    expect(
        readJSONFile(path.join(process.cwd(), 'guetrc.json')).committers
    ).toEqual([
        {
            email: 'first@example.com',
            fullName: 'first',
            initials: 'f',
        },
    ]);
});
