# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG NODE_VERSION=20.9.0

################################################################################
# Use node image for base image for all stages.
FROM node:${NODE_VERSION}-alpine AS base

# Set working directory for all build stages.
WORKDIR /usr/src/app

RUN npm install -g npm@~10.x.x

################################################################################
# Create a stage for building the application.
FROM base AS build

# Download additional development dependencies before building, as some projects require
# "devDependencies" to be installed to build. If you don't need this, remove this step.
# RUN --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     --mount=type=cache,target=/root/.npm \
#     npm ci
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the source files into the image.
COPY . .

ENV NODE_ENV=production

# Run the build script.
RUN npm run build

################################################################################
# Create a new stage to run the application with minimal runtime dependencies
# where the necessary files are copied from the build stage.
# Use nginx image to serve the static site
FROM nginx:1.25.3-alpine-slim AS runtime

# Copy the static assets from the build image
COPY --from=build /usr/src/app/build /usr/share/nginx/html

# Optional: Copy a custom nginx configuration (if you have one)
COPY nginx/nginx.conf /etc/nginx/templates/default.conf.template

EXPOSE 80

ENV NGINX_PORT=80

CMD ["nginx", "-g", "daemon off;"]
