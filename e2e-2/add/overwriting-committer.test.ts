import colors from 'colors';

import { configPath, readJSONFile } from '../../src/utils';
import { assembleOutput, run } from '../utils';

colors.enable();

test("it should alert user that they're overwritting a committer, and give them the option to force it", () => {
    run('guet init');
    run('guet add fn "first name1" firstname@example.com');

    const [firstOut, statusCode] = run(
        'guet add fn "first name2" firstname@example.com'
    );

    expect(firstOut).toEqual(
        assembleOutput([
            'Failed to write "fn" "first name2" "firstname@example.com" because it would overwrite already present committer: "fn" "first name1" "firstname@example.com"'
                .red,
            'You can force this overwrite by adding the --force flag.'.red,
        ])
    );

    expect(statusCode).toEqual(1);

    const [secondOut] = run(
        'guet add fn "first name2" firstname@example.com --force'
    );

    const found = readJSONFile(configPath);
    expect(found.committers).toHaveLength(1);
    expect(found.committers[0]).toEqual({
        email: 'firstname@example.com',
        fullName: 'first name2',
        initials: 'fn',
    });

    expect(secondOut).toEqual(
        assembleOutput([
            'Overwritting previous committer with initials "fn".'.green,
        ])
    );
});
