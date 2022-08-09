import fs from 'fs';
import { homedir } from 'os';
import path from 'path';

export function init(_args: string[]) {
    console.log('running init');
    const configDir = path.join(homedir(), '.guet');
    if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir);
    }
}
