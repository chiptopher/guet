abstract class ChainLink {
    following?: ChainLink;

    execute(args: string[]) {
        this.doExecute(args);
        if (this.following) {
            this.following.execute(args);
        }
    }

    public next(link: ChainLink) {
        if (!this.following) {
            this.following = link;
        } else {
            let current = this.following;
            while (current.following !== undefined) {
                current = current.following;
            }
            current.following = link;
        }
        return this;
    }

    protected abstract doExecute(args: string[]): void;
}

export { ChainLink };
