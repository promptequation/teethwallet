FROM node:lts
ENV HOST=0.0.0.0
ENV PORT=3000
ENV NODE_OPTIONS=--max_old_space_size=4096
WORKDIR /app

COPY . .

RUN cd ./website && yarn install
RUN cd ./website && yarn build

EXPOSE 3000

ARG COMMIT_ID
ARG PROJECT_VERSION
ENV PROJECT_VERSION="${PROJECT_VERSION}"

LABEL org.opencontainers.image.title="promptequation/oral-ehealth-frontend"               \
      org.opencontainers.image.description="headless oral e-health framework,"            \
      org.opencontainers.image.url="https://www.promptequation.com/"                      \
      org.opencontainers.image.source="https://github.com/odoogap/oehealth"               \
      org.opencontainers.image.revision="$COMMIT_ID"                                      \
      org.opencontainers.image.version="$PROJECT_VERSION"                                 \
      org.opencontainers.image.authors="PROMPTEquation (https://www.promptequation.com)"  \
      org.opencontainers.image.licenses="BSD 3"

WORKDIR /app/website

CMD [ "yarn", "start" ]
