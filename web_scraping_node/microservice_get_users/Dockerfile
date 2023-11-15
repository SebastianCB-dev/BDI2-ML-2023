FROM node:20.9.0-alpine as development-dependencies
WORKDIR /app
RUN npm install --location=global pnpm
COPY package.json package-lock.yaml ./
RUN pnpm install

FROM node:20.9.0-alpine as production-dependencies
WORKDIR /app
RUN npm install --location=global pnpm
COPY package.json package-lock.yaml ./
RUN pnpm install --production

FROM node:20.9.0-alpine as builder
WORKDIR /app
RUN npm install --location=global pnpm
COPY --from=development-dependencies /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM node:20.9.0-alpine as production
WORKDIR /app
RUN npm install --location=global pnpm
COPY --from=production-dependencies /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]

