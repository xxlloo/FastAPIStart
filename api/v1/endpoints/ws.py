from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

ws_router = APIRouter(
    prefix="/ws",

)

# 存储所有连接的客户端
connected_clients: List[WebSocket] = []


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()

            # 打印接收到的消息
            print(f"收到来自 {client_id} 的消息: {data}")

            # 回显消息（简单示例）
            await websocket.send_text(f"服务器已收到消息: {data}")

            # 广播给所有客户端（扩展功能）
            # await broadcast(message=f"Client {client_id} says: {data}")

    except WebSocketDisconnect:
        # 处理客户端断开连接
        connected_clients.remove(websocket)
        print(f"客户端 {client_id} 断开连接")
        print(f"当前连接数: {len(connected_clients)}")
    except Exception as e:
        print(f"处理 {client_id} 消息时发生错误: {str(e)}")


# 扩展功能：广播消息给所有客户端
async def broadcast(message: str):
    for client in connected_clients[:]:  # 创建副本避免修改列表异常
        try:
            await client.send_text(message)
        except WebSocketDisconnect:
            connected_clients.remove(client)
