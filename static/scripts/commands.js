var socket = io();

socket.on('server_output', function(data) {
    var terminal = document.getElementById('terminal');
    terminal.innerText += "> " + data.output + "\n";
    terminal.scrollTop = terminal.scrollHeight;
});

document.getElementById('command_form').addEventListener("submit", (event)=> {
    event.preventDefault();
    var command = document.getElementById('commandInput').value;
    socket.emit('send_command', {"command": command});
    document.getElementById('commandInput').value = '';
});