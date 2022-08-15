import { CommandExecutor } from './command-executor';
import { addCommand } from './commands/add';
import { getCommand } from './commands/get';
import { hookCommand } from './commands/hook';
import { initCommand } from './commands/init';
import { removeCommand } from './commands/remove';
import { setComand } from './commands/set';
import { version } from './version';

export function executeCommand(commandName: string, args: string[]) {
    const executor = new CommandExecutor([
        setComand,
        getCommand,
        addCommand,
        removeCommand,
        initCommand,
        hookCommand,
    ]);

    switch (commandName) {
        case '--version':
        case '-v':
            return version();
        default:
            executor.evaluate([commandName, ...args]);
    }
}
