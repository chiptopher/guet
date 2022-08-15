import path from 'path';

import { ClosureChainLink, Command } from './command';
import { CommandExecutor } from './command-executor';
import { readJSONFile } from './utils';

describe('CommandExecutor', () => {
    it('should execute command with matching identifier', () => {
        const command: any = {
            execute: jest.fn(),
            identifier: 'name',
        };

        const commandExecutor = new CommandExecutor([command]);
        commandExecutor.evaluate(['name', 'rest']);
        expect(command.execute).toHaveBeenCalledWith(['rest']);
    });

    it("should call the command's help message when there's a help flag", () => {
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        const log = jest.spyOn(console, 'log').mockImplementation(() => {});
        const func = jest.fn();
        const command = new Command(
            'name',
            { description: 'description', usage: 'usage' },
            new ClosureChainLink(func)
        );

        const commandExecutor = new CommandExecutor([command]);

        commandExecutor.evaluate(['name', 'rest', '--help']);

        expect(func).not.toHaveBeenCalled();
        expect(log).toHaveBeenCalledWith(command.helpMessage('long'));

        log.mockReset();
    });

    it('prints the version when --version / -v is present', () => {
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        const log = jest.spyOn(console, 'log').mockImplementation(() => {});
        const func = jest.fn();
        const command = new Command(
            'name',
            { description: 'description', usage: 'usage' },
            new ClosureChainLink(func)
        );

        const commandExecutor = new CommandExecutor([command]);

        commandExecutor.evaluate(['--version']);

        const version = readJSONFile(
            path.join(__dirname, '..', 'package.json')
        ).version;

        expect(func).not.toHaveBeenCalled();
        expect(log).toHaveBeenCalledWith(version);

        log.mockReset();

        commandExecutor.evaluate(['-v']);
        expect(func).not.toHaveBeenCalled();
        expect(log).toHaveBeenCalledWith(version);
    });
});
