import { configPath, readJSONFile } from '../../src/utils';
import { run } from '../utils';

test('adding committer will create a config folder if necessary', () => {
    run('guet add f first first@example.com');

    const found = readJSONFile(configPath);
    expect(found.committers).toEqual([
        {
            email: 'first@example.com',
            fullName: 'first',
            // thier initials should be lowercased when added
            initials: 'f',
        },
    ]);
});
