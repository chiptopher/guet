import path from 'path';

import { readJSONFile } from './utils';

export function version() {
    console.log(
        readJSONFile(path.join(__dirname, '..', 'package.json')).version
    );
}
