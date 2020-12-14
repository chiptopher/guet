import { GluegunCommand } from 'gluegun';
import { projectRoot } from '../util/projectRoot';

const command: GluegunCommand = {
    name: 'guet',
    run: async toolbox => {
        const { print } = toolbox;
        print.info(`Welcome to your CLI ${projectRoot()}`);
    },
};

module.exports = command;
