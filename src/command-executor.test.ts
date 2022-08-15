import { ClosureChainLink, Command } from './command';
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
});
