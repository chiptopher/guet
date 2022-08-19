import path from 'path';

import { log } from './native-wrapper';
import { readJSONFile } from './utils';

export function version() {
    log(readJSONFile(path.join(__dirname, '..', 'package.json')).version);
}
