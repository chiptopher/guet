import { execSync } from 'child_process';
import fs from 'fs';
import { homedir } from 'os';
import path from 'path';

describe('guet init', () => {
    it('should create a guet config folder in the root directory', () => {
        execSync('npm run test:run init');
        expect(fs.existsSync(path.join(homedir(), '.guet'))).toEqual(true);
    });
});
