import { Command } from './command';

export class CommandExecutor {
    private commands: Command[];

    constructor(commands: Command[]) {
        this.commands = commands;
    }

    public evaluate(args: string[]): void {
        const [commandName, ...rest] = args;

        const found = this.commands.find(
            command => command.identifier === commandName
        );

        if (found) {
            if (rest.includes('--help')) {
                console.log(found.helpMessage('long'));
            } else {
                found.execute(rest);
            }
        }
    }
}
