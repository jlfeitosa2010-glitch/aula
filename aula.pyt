from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Lista simples em memória para salvar os usuários
usuarios = []


class ServidorSite(BaseHTTPRequestHandler):

    # Serve a página HTML quando alguém entra no site
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open("index.html", "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))

        elif self.path == "/style.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()

            with open("style.css", "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))

    # Recebe as informações quando o botão do formulário é clicado
    def do_POST(self):
        if self.path == "/salvar":
            # Lê o tamanho dos dados
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")

            # Converte os dados do formulário
            campos = parse_qs(dados)

            # Salva na lista do Python
            novo_usuario = {
                "nome": campos["nome"][0],
                "idade": campos["idade"][0],
                "email": campos["email"][0],
                "senha": campos["senha"][0],
            }
            usuarios.append(novo_usuario)

            # Mostra no terminal
            print("\n--- Novo Cadastro ---")
            print(novo_usuario)

            # Envia a resposta de confirmação para o navegador
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            resposta = f"""
            <h2>Cadastro Realizado com Sucesso!</h2>
            <p><strong>Nome:</strong> {novo_usuario['nome']}</p>
            <p><strong>Idade:</strong> {novo_usuario['idade']} anos</p>
            <p><strong>E-mail:</strong> {novo_usuario['email']}</p>
            <a href="/">Voltar</a>
            """
            self.wfile.write(resposta.encode("utf-8"))


# Inicia o servidor
servidor = HTTPServer(("localhost", 8000), ServidorSite)
print("Site rodando em http://localhost:8000")
servidor.serve_forever()
