import { CommandExecutor } from './command-executor';

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
        const command: any = {
            execute: jest.fn(),
            help: {
                long: 'long help message',
            },
            identifier: 'name',
        };

        const commandExecutor = new CommandExecutor([command]);

        commandExecutor.evaluate(['name', 'rest', '--help']);

        expect(command.execute).not.toHaveBeenCalled();
        expect(log).toHaveBeenCalledWith(command.help.long);

        log.mockReset();
    });
});
