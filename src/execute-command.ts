export function executeCommand(commandName: string, args: string[]) {
    console.log(commandName);
    args.forEach(console.log);
}
