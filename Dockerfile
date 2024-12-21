FROM nikolaik/python-nodejs:python3.11-nodejs23-alpine AS base

FROM base AS builder
WORKDIR /app/frontend
COPY ./frontend .
RUN npm install
RUN npm run build

FROM base AS runner
WORKDIR /app/backend
COPY ./backend .
RUN pip3 install --no-cache-dir -r requirements.txt
WORKDIR /app/frontend
COPY --from=builder /app/frontend/.next/static ./.next/static
COPY --from=builder /app/frontend/.next/standalone ./

WORKDIR /app
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 5000
EXPOSE 3000
CMD ["/start.sh"]
