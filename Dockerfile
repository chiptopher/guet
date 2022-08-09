FROM node:18-slim
COPY . ./test

WORKDIR test
RUN npm run test:e2e:execute
