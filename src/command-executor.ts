import path from 'path';

import { Command } from './command';
import { log } from './native-wrapper';
import { readJSONFile } from './utils';

export class CommandExecutor {
    private commands: Command[];

    constructor(commands: Command[]) {
        this.commands = commands;
    }

    public evaluate(args: string[]): void {
        const [commandName, ...rest] = args;
        if (
            commandName === undefined ||
            commandName === '--help' ||
            commandName === '-h'
        ) {
            log(this.buildHelpMessage());
            process.exit(0);
        }
        if (['--version', '-v'].includes(commandName)) {
            const version = readJSONFile(
                path.join(__dirname, '..', 'package.json')
            ).version;

            log(version);
        } else {
            const found = this.commands.find(
                command => command.identifier === commandName
            );

            if (found) {
                if (rest.includes('--help')) {
                    log(found.helpMessage('long'));
                } else {
                    found.execute(rest);
                }
            } else {
                log(this.buildHelpMessage());
            }
        }
    }

    buildHelpMessage(): string {
        const commandsWithDescriptions = this.commands
            .map(
                command =>
                    `${command.identifier}: ${command.helpMessage('short')}`
            )
            .join('\n');
        return `usage: guet <command>\n\n${commandsWithDescriptions}`;
    }
}
