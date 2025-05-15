const menuItems = document.querySelectorAll('.item-menu');
const chat = document.querySelector(".chat");
const chatMessages = chat.querySelector(".chat__messages");
const chatForm = chat.querySelector(".chat__form");
const chatInput = chat.querySelector(".chat__input");

// Definindo um nome de usuário padrão caso 'window.nomeUsuario' não esteja definido
window.nomeUsuario = window.nomeUsuario || "Usuário Desconhecido"; // Garantir que tenha um nome de usuário

// Função para selecionar ícone de menu
function selectIcon() {
    menuItems.forEach((item) => item.classList.remove('ativo'));
    this.classList.add('ativo');
}

menuItems.forEach((item) => {
    item.addEventListener('click', selectIcon);
});

// Funcionalidade de expandir/contrair menu lateral
const btnExp = document.getElementById('btn-exp');
const menuLateral = document.querySelector('.menu-lateral');

btnExp.addEventListener('click', () => {
    menuLateral.classList.toggle('expandir');
    document.body.classList.toggle('menu-expandido');
});

chat.style.display = "flex";

// Conectar ao servidor Socket.IO
const socket = io.connect("http://127.0.0.1:5000/");

// Evento para quando a conexão for estabelecida
socket.on('connect', function() {
    console.log("Conectado ao servidor Socket.IO!");
});

// Evento para receber mensagens (no servidor, deve enviar a mensagem a todos, exceto o remetente)
socket.on('message', function(msg) {
    console.log("Mensagem recebida:", msg);
    
    // Verifica se a mensagem não é sua (ou seja, não é a mesma que você enviou)
    if (msg.sender && msg.sender !== window.nomeUsuario) { // Garantir que 'sender' exista
        const messageElement = document.createElement("div");
        messageElement.classList.add("message-other");
        messageElement.innerText = msg.text;
        
        // Adicionar a mensagem à área do chat
        chatMessages.appendChild(messageElement);
        
        // Salvar as mensagens no localStorage
        saveMessages();
        
        // Rolar para o final do chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

// Enviar mensagem
chatForm.addEventListener('submit', function(event) {
    event.preventDefault();  // Impede o envio do formulário

    const message = chatInput.value.trim();
    if (message) {
        console.log("Enviando mensagem:", message);

        // Enviar a mensagem para o servidor Socket.IO
        socket.send({ text: message, sender: window.nomeUsuario });

        // Adicionar a mensagem à área do chat (para visualização imediata)
        const messageElement = document.createElement("div");
        messageElement.classList.add("message--self");
        messageElement.innerText = message;
        chatMessages.appendChild(messageElement);

        // Salvar as mensagens no localStorage
        saveMessages();

        // Limpar o campo de input
        chatInput.value = "";

        // Rolar para o final do chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

// Função para salvar as mensagens no localStorage
function saveMessages() {
    const messages = [];
    const messageElements = chatMessages.querySelectorAll(".message--self, .message-other");
    messageElements.forEach((element) => {
        messages.push({
            text: element.innerText,
            class: element.classList.contains("message--self") ? "message--self" : "message-other"
        });
    });
    localStorage.setItem('messages', JSON.stringify(messages));
}

// Função para carregar as mensagens do localStorage
function loadMessages() {
    const savedMessages = JSON.parse(localStorage.getItem('messages'));
    if (savedMessages && Array.isArray(savedMessages)) {  // Verificar se as mensagens são válidas
        savedMessages.forEach((msg) => {
            const messageElement = document.createElement("div");
            messageElement.classList.add(msg.class);
            messageElement.innerText = msg.text;
            chatMessages.appendChild(messageElement);
        });
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Carregar as mensagens ao iniciar
loadMessages();
