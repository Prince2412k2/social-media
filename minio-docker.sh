docker run -p 9000:9000 -p 9001:9001 \
  --name minio \
  -e "MINIO_ROOT_USER=123456789" \
  -e "MINIO_ROOT_PASSWORD=123456789" \
  -v $(pwd)/data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
