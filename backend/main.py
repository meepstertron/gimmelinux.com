import random
from fastapi import FastAPI, WebSocket
import docker
from starlette.websockets import WebSocketState
import asyncio
import collections

MAX_CONTAINERS = 2
VERSION = "0.1.0"
TEXTS = [
        "Bash for the people!",
        "69 lonely shells in your terminal",
        "Now with 100% less php",
        "Docking to the port",
        ""
    ]

motd = f"""
gimmelinux.com - {random.choice(TEXTS)} \r
powered by hexagonical.xyz
"""
active_containers = 0
queue = collections.deque()
queue_lock = asyncio.Lock()


app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global active_containers
    await websocket.accept()
    

    


    await websocket.send_text(f"{motd}\r\n")


    async with queue_lock:
        queue.append(websocket)


    while True:
        async with queue_lock:
            is_first = queue[0] == websocket
            can_start = active_containers < MAX_CONTAINERS
        if is_first and can_start:
            break
        await websocket.send_text(f"Waiting for your turn... [{queue.index(websocket) + 1}/{len(queue)}]\r\n")
        await asyncio.sleep(5)


    async with queue_lock:
        queue.popleft()
        active_containers += 1
    
    docker_client = docker.from_env()
    container = None
    try:
        container = docker_client.containers.run(
            "alpine:latest",
            command="sh",
            detach=True,
            tty=True,
            stdin_open=True,
            auto_remove=True,
        )
        await websocket.send_text(f"Container started, attaching...\r\n")
        

        sock = container.attach_socket(params={'stdin': 1, 'stdout': 1, 'stderr': 1, 'stream': 1, 'logs': 1})
        sock._sock.setblocking(False)
        
        sock._sock.sendall("\n".encode())

        async def read_from_container():
            while websocket.application_state == WebSocketState.CONNECTED:
                try:
                    output = sock._sock.recv(4096).decode()
                except BlockingIOError:
                    output = ""
                if output:
                    await websocket.send_text(output)
                await asyncio.sleep(0.01)

        async def read_from_websocket():
            while websocket.application_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()
                try:
                    sock._sock.sendall(data.encode())
                except Exception as e:
                    await websocket.send_text(f"Error occurred while sending command: {e}")

        await asyncio.gather(
            read_from_container(),
            read_from_websocket()
        )

    except Exception as e:
        await websocket.send_text(f"Error occurred: {e}, closing connection")
    finally:
        async with queue_lock:
            active_containers -= 1
        try:
            await websocket.close()
        except Exception:
            pass
        if container:
            try:
                container.kill()
            except Exception:
                pass
            try:
                container.remove(force=True)
            except Exception:
                pass
        docker_client.close()