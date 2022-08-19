import { CommandExecutor } from './command-executor';
import { addCommand } from './commands/add';
import { getCommand } from './commands/get';
import { hookCommand } from './commands/hook';
import { initCommand } from './commands/init';
import { removeCommand } from './commands/remove';
import { setComand } from './commands/set';
import { yeetCommand } from './commands/yeet';

export function executeCommand(commandName: string, args: string[]) {
    const executor = new CommandExecutor([
        setComand,
        getCommand,
        addCommand,
        removeCommand,
        initCommand,
        yeetCommand,
        hookCommand,
    ]);

    executor.evaluate([commandName, ...args]);
}
