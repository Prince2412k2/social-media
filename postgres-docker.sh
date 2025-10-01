docker run -d \
  --name bookish \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=12345678 \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  postgres:16
