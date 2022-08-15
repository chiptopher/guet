import fs from 'fs';

import { ChainLink } from '.';
import { emptyConfig } from '../config';
import { configPath, writeConfig } from '../utils';

export class Initialize extends ChainLink {
    protected doExecute(_: string[]): void {
        if (!fs.existsSync(configPath)) {
            writeConfig(emptyConfig());
        }
    }
}
