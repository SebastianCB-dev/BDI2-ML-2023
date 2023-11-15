# Building stage
FROM node:20.9.0-alpine as builder
WORKDIR /app
RUN npm install --global pnpm
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# Final stage
FROM node:20.9.0-alpine as production
WORKDIR /app
RUN npm install --global pnpm
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --production
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
