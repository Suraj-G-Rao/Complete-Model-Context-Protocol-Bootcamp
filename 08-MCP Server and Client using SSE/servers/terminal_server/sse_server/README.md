docker build -t terminal_server_sse .

docker run --rm -p 8081:8081 -v C:/Users/AC/mcp/workspace:/root/mcp/workspace terminal_server_sse