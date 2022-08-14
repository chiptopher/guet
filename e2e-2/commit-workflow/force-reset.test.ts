import { DateTime } from 'luxon';

import { readRepoConfig, writeRepoConfig } from '../../src/utils';
import { run } from '../utils';

test('blocks commit unless "guet reset" is called', () => {
    run('git init');
    run('guet init --withHooks');

    run('guet add f first first@example.com');
    run('guet add s second second@example.com');
    run('guet set f s');

    const now = DateTime.now().minus({ hours: 24 });

    const config = readRepoConfig();
    config.setTime = now.toISO();
    writeRepoConfig(config);

    run('git add .');
    run('git commit -m "Initial commit"');

    const [output] = run('git log');
    expect(output).toEqual(
        "fatal: your current branch 'main' does not have any commits yet\n"
    );
});
