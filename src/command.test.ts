import { Command } from './command';

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
                `${help.description}\n${help.usage}`
            );
        });
    });
});
