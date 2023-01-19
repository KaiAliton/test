import json

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()
html = """
<head>
    <title>Test</title>
</head>
<style>
    .chat-wrapper {
    background: #2f323b;
    width: 50%;
    margin: 0 auto;
    }
    
    .chat-container {
    height: 500px;
    width: 100%;
    display: flex;
    overflow: auto;
    flex-direction: column;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: center;
    }
    
    .chat-container::-webkit-scrollbar {
    display: none;
    }
    
    .message {
    padding: 5px;
    border-radius: 6px 0 0 6px;
    background: #2671ff;
    margin-top: 0.3rem;
    margin-bottom: 0.3rem;
    display: inline-block;
    font-size: 32px;
    width: fit-content;
    max-width: 70%;
    hyphens: manual;
    align-self: flex-end;
    }
    
    .message span {
    word-wrap: break-word;
    max-width: calc(100% - 50px);
    }
    
    .chat-message form {
    width: 100%;
    display: flex;
    flex-direction: row;
    }
    
    form input {
    height: 59px;
    line-height: 60px;
    outline: 0 none;
    border: none;
    flex-basis: 90%;
    }
    
    form button {
    background: none;
    border: none;
    border-left: 1px solid #2671ff;
    flex-basis: 10%;
    }
    
    .message:nth-child(2n) {
    background: #5b5e6c;
    border-radius: 0 6px 6px 0;
    align-self: flex-start;
    color: #fff;
    }
</style>
<body>
    <div class="chat-wrapper">
        <div class="chat-container" id="messages">
        </div>
        <div class="chat-message">
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off" />
                <button>Отправить</button>
            </form>
        </div>
    </div>
    <script>
        var ws = new WebSocket("ws://localhost:8000/ws");
        ws.onmessage = function (event) {
            var json = JSON.parse(event.data)
            var messages = document.getElementById('messages')
            var messagebox = document.createElement('div')
            messagebox.classList.add('message')
            var messagetext = document.createElement('span')
            var content = document.createTextNode(json['id'] + ":" + json['response'])
            messagetext.appendChild(content)
            messagebox.appendChild(messagetext)
            messages.appendChild(messagebox)
        };
        function sendMessage(event) {
            var input = document.getElementById("messageText")
            message = JSON.stringify({text: input.value})
            ws.send(message)
            input.value = ''
            event.preventDefault()
        }
    </script>
</body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    counter = 0
    while True:
        data = await websocket.receive_json()
        if data['text'] == "":
            continue
        counter = counter + 1
        response ={
            'id': counter,
            'response': data['text']
        }
        await websocket.send_json(response)
