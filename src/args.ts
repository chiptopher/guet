export function separateFlags(args: string[]): [string[], string[]] {
    const isFlag = (arg: string) => arg.startsWith('--');

    const flags = args.filter(isFlag);
    const notFlags = args.filter(arg => !isFlag(arg));

    return [notFlags, flags];
}
