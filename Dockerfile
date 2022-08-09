FROM node:18
COPY . ./test
WORKDIR test
RUN npm link
