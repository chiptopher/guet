import { CommandExecutor } from './command-executor';
import { add } from './commands/add';
import { getCommand } from './commands/get';
import { hook } from './commands/hook';
import { init } from './commands/init';
import { remove } from './commands/remove';
import { setComand } from './commands/set';
import { version } from './version';

export function executeCommand(commandName: string, args: string[]) {
    const executor = new CommandExecutor([setComand, getCommand]);

    switch (commandName) {
        case '--version':
        case '-v':
            return version();
        case 'init':
            return init(args);
        case 'add':
            return add(args);
        case 'hook':
            return hook(args);
        case 'remove':
            return remove(args);
        default:
            executor.evaluate([commandName, ...args]);
    }
}
