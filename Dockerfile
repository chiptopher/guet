FROM node:18
COPY . ./test
WORKDIR test
RUN git config --global init.defaultBranch main
RUN npm link
