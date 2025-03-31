
# 🛠️ Projeto Django - CD MDF Móveis

Este é um sistema desenvolvido em **Django** para gerenciar dados de um centro de distribuição. O sistema oferece funcionalidades de CRUD, controle de usuários e diversas outras interações de gerenciamento.

---

## 🚀 Tecnologias Utilizadas

- **🧩 Django**: Framework web Python.
- **🎨 Bootstrap**: Framework CSS para criar interfaces responsivas.
- **📊 jQuery e DataTables**: Biblioteca JavaScript para melhorar a interação com tabelas.
- **⭐ Font Awesome**: Para ícones e elementos gráficos.
- **📝 Cleave.js**: Biblioteca JavaScript para formatação de campos de entrada.
- **🐘 PostgreSQL**: Banco de dados utilizado no projeto.

---

## 🗂️ Estrutura do Projeto

A estrutura do projeto está organizada conforme o modelo tradicional:

```
├───cadastros
├───colaboradores
├───fornecedores
├───frota
├───seguranca
```

Cada diretório corresponde a um módulo da aplicação, com arquivos responsáveis por:

- **📄 models.py**: Definição das tabelas no banco de dados.
- **👨‍💻 views.py**: Funções que gerenciam as interações com o usuário.
- **🔗 urls.py**: Mapeamento das URLs da aplicação.
- **📁 templates**: Arquivos HTML para renderizar as páginas.
- **🗃️ migrations**: Arquivos para controle de mudanças no banco de dados.

---

## 🏃‍♂️ Como Rodar o Projeto

### 1️⃣ Clonando o Repositório

Primeiro, clone o repositório para o seu computador:

```bash
git clone https://github.com/rb-alves/cd-mdf-moveis.git .
```

---

### 2️⃣ Criando o Ambiente Virtual

Para garantir que as dependências sejam instaladas de forma isolada, é recomendado usar um ambiente virtual.

**Crie o ambiente virtual:**

```bash
python -m venv .venv
```

**Ative o ambiente virtual:**

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

---

### 3️⃣ Instalando as Dependências

Após ativar o ambiente virtual, instale as dependências do projeto listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configurando as Variáveis de Ambiente

Crie uma cópia do arquivo `.env.example` e renomeie para `.env`:

```bash
cp .env.example .env
```

No arquivo `.env`, insira o valor das variáveis de ambiente, como o nome do banco, usuário e senha. 

Exemplo de configuração do arquivo `.env`:

```env
# Django Variáveis
SECRET_KEY=uma_chave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, .seusite.com

# Banco de Dados
DB_NAME=nome_do_banco
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
DB_HOST=localhost
DB_PORT=5432

# Configurações de e-mail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_email
DEFAULT_FROM_EMAIL=seu_email@gmail.com
```

---

### 5️⃣ Migrando o Banco de Dados

Execute as migrações para configurar o banco de dados:

```bash
python manage.py migrate
```

---

### 6️⃣ Rodando o Servidor

Por fim, inicie o servidor de desenvolvimento do Django:

```bash
python manage.py runserver
```

---

💡 **Dica Extra**: Consulte sempre a documentação oficial do Django para dúvidas adicionais. Boas práticas e configurações específicas para produção estão bem detalhadas lá.

---
