import asyncio
import websockets

# WebSocket 服务器
async def handler(websocket, path):
    print("A client just connected")
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            response = f"Server received your message: {message}"
            await websocket.send(response)
    finally:
        print("Client disconnected")

async def start_server():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Server started on ws://localhost:8765")
    await server.wait_closed()

# WebSocket 客户端
async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter a message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received response from server: {response}")

# 运行服务器和客户端
async def main():
    server_task = asyncio.create_task(start_server())
    await asyncio.sleep(1)  # 给服务器一些启动时间
    
    client_task = asyncio.create_task(client())
    
    await asyncio.gather(server_task, client_task)

if __name__ == "__main__":
    asyncio.run(main())