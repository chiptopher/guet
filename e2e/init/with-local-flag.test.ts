import { existsSync } from 'fs';
import path from 'path';

import { run } from '../utils';

test('when --local is provided it puts an in-repo config file', () => {
    run('git init');
    run('guet init --local');
    expect(existsSync(path.join(process.cwd(), 'guetrc.json'))).toEqual(true);
});
