import path from 'path';

import { Command } from './command';
import { readJSONFile } from './utils';

export class CommandExecutor {
    private commands: Command[];

    constructor(commands: Command[]) {
        this.commands = commands;
    }

    public evaluate(args: string[]): void {
        const [commandName, ...rest] = args;
        if (['--version', '-v'].includes(commandName)) {
            const version = readJSONFile(
                path.join(__dirname, '..', 'package.json')
            ).version;

            console.log(version);
        } else {
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
}
