import { exec } from 'child_process';
import fs from 'fs';

describe('guet init', () => {
    it('should create a guet config folder in the root directory', () => {
        exec('npm run test:run init');
        expect(fs.existsSync('~/.guet')).toEqual(true);
    });
});
