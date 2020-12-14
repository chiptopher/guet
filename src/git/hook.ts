import { filesystem } from 'gluegun';

export enum HookName {
    PreCommit = 'pre-commit',
    PostCommit = 'post-commit',
    CommitMsg = 'commit-msg',
}

export class Hook {
    private gitPath: string;
    private name: HookName;
    constructor(gitPath: string, name: HookName) {
        this.gitPath = gitPath;
        this.name = name;
    }

    public exists(): boolean {
        return filesystem.exists(this.hookpath()) ? true : false;
    }

    private hookpath(): string {
        return filesystem.path(this.gitPath, 'hooks', this.name);
    }
}
