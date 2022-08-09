#!/usr/bin/env node

import colors from 'colors';
import { config } from 'dotenv';

import { executeCommand } from './execute-command';

config();
colors.enable();

async function main() {
    const [_, _2, commandName, ...rest] = process.argv;
    return executeCommand(commandName, rest);
}

main().catch(err => console.error(err));
