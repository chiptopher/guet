FROM node:18
COPY . ./test
WORKDIR test
RUN git config --global init.defaultBranch main
RUN git config --global user.email "you@example.com"
RUN git config --global user.name "Your Name"
RUN npm run build
RUN npm link
