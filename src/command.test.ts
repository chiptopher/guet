/* eslint-disable @typescript-eslint/no-empty-function */

import { ClosureChainLink, Command } from './command';

describe('Command', () => {
    describe('helpMessage', () => {
        it('should return currect message for size', () => {
            const links: any = {};
            const help = {
                description: 'description',
                usage: 'usage',
            };
            const command = new Command('name', help, links);
            expect(command.helpMessage('short')).toEqual(help.description);
            expect(command.helpMessage('long')).toEqual(
                `${help.description}\nusage: ${help.usage}`
            );
        });
    });

    describe('execute', () => {
        it('prints the help message when no args are given if `printHelpOnNoArgs` is set to true and there are no args', () => {
            const log = jest.spyOn(console, 'log').mockImplementation(() => {});
            const exit = jest
                .spyOn(process, 'exit')

                .mockImplementation(((_: any) => {}) as any);
            const command = new Command(
                '',
                {
                    description: 'description',
                    usage: 'usage',
                },
                new ClosureChainLink(() => {}),
                true
            );

            command.execute(['arg']);

            expect(log).not.toHaveBeenCalled();
            expect(exit).not.toHaveBeenCalled();

            command.execute([]);

            expect(log).toHaveBeenCalledWith(command.helpMessage('long'));
            expect(exit).toHaveBeenCalledWith(1);

            log.mockReset();
            exit.mockReset();
        });
    });
});
