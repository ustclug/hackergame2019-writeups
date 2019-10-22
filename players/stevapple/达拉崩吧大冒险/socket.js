var socket = $socket.new("ws://202.38.93.241:10021/ws");
$ui.render({
  props: {
    title: "达拉崩吧"
  },
  views: [
    {
      type: "input",
      props: {
        placeholder: "Message"
      },
      layout: (make, view) => {
        make.top.right.left.inset(10);
        make.height.equalTo(36);
      },
      events: {
        ready: (sender) => {
          sender.focus();
        },
        returned: (sender) => {
          var text = sender.text;
          sender.text = "";
          sendMessage(text);
        }
      }
    }
  ]
});
function sendMessage(message) {
  socket.send(message);
  console.log(`Sent: ${message}`);
}
var events = {};
events.didOpen = (sock) => {
  console.log("Websocket Connected");
}
events.didFail = (sock, error) => {
  console.log(`:( Websocket Failed With Error: ${error}`);
}
events.didClose = (sock, code, reason, wasClean) => {
  console.log("Websocket closed");
}
events.didReceiveString = (sock, string) => {
  console.log(`Received: ${string}`);
}
events.didReceivePing = (sock, data) => {
  console.log("Websocket received ping");
}
events.didReceivePong = (sock, data) => {
  console.log("Websocket received pong");
}
socket.listen(events);
socket.open();
console.log("Connecting...");