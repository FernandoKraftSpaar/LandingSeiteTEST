# Guia de Configuração da API DAB (Data Access Builder)

Este guia ajuda a configurar corretamente a conexão do DAB com Azure SQL Database para eliminar os erros 400 e 500 no dashboard.

## 🔍 Problema Identificado

O erro ocorre porque a string de conexão no `.env.example` estava no formato SQLAlchemy (Python) em vez do formato esperado pelo DAB (.NET/SQL Server).

### ❌ Formato Incorreto (SQLAlchemy)
```
mssql+pyodbc://smartspaaroperation.database.windows.net:1433/DBNAME?driver=ODBC+Driver+18+for+SQL+Server
```

### ✅ Formato Correto (SQL Server Connection String)
```
Server=smartspaaroperation.database.windows.net,1433;Database=YOUR_DATABASE_NAME;User Id=YOUR_USERNAME;Password=YOUR_PASSWORD;Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;
```

## 🛠️ Configuração Passo a Passo

### 1. Configurar Variáveis de Ambiente

1. **Localmente** (para desenvolvimento):
   - Copie `.env.example` para `.env`
   - Substitua os valores placeholder pelos dados reais do seu banco

2. **Azure Static Web Apps** (produção):
   - Vá ao portal Azure → seu Static Web App → Configuration
   - Adicione a variável `DATABASE_CONNECTION_STRING` com o valor correto

### 2. Formatos de Connection String Disponíveis

#### Opção 1: Autenticação SQL (mais comum)
```
Server=smartspaaroperation.database.windows.net,1433;Database=SEU_BANCO;User Id=SEU_USUARIO;Password=SUA_SENHA;Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;
```

#### Opção 2: Azure AD Authentication (recomendado para produção)
```
Server=smartspaaroperation.database.windows.net,1433;Database=SEU_BANCO;Authentication=Active Directory Default;Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;
```

#### Opção 3: Com otimizações de pool de conexão
```
Server=smartspaaroperation.database.windows.net,1433;Database=SEU_BANCO;User Id=SEU_USUARIO;Password=SUA_SENHA;Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;Max Pool Size=100;Min Pool Size=5;
```

### 3. Configuração do Banco de Dados

Certifique-se que sua tabela existe com a estrutura esperada:

```sql
CREATE TABLE dbo.equipamentos (
    id int IDENTITY(1,1) PRIMARY KEY,
    nome nvarchar(255) NOT NULL,
    potencia decimal(10,2) NOT NULL,
    horas_uso decimal(5,2) NOT NULL,
    categoria nvarchar(100),
    idade int,
    etiqueta_eficiencia nvarchar(50),
    observacoes nvarchar(max),
    tag nvarchar(100),
    fator_correcao decimal(5,2) DEFAULT 1.00,
    op_hora_ini time,
    op_hora_fim time,
    connected_to nvarchar(100),
    created_at datetime2 DEFAULT GETDATE(),
    updated_at datetime2 DEFAULT GETDATE()
);
```

### 4. Verificação da Configuração DAB

O arquivo `swa-db-connections/staticwebapp.database.config.json` está configurado corretamente:

- ✅ Database type: `mssql`
- ✅ Connection string: `@env('DATABASE_CONNECTION_STRING')`
- ✅ REST endpoint: `/rest`
- ✅ GraphQL endpoint: `/graphql`
- ✅ Entity: `Equipamento` → `dbo.equipamentos`

## 🧪 Testando a Configuração

### 1. Testar Localmente com SWA CLI

```bash
# Instalar SWA CLI
npm install -g @azure/static-web-apps-cli

# Executar localmente
swa start . --data-api-location swa-db-connections
```

### 2. Testar Endpoints da API

#### Listar equipamentos (GET)
```bash
curl -X GET "https://SEU_SITE.azurestaticapps.net/data-api/rest/Equipamento" \
  -H "Accept: application/json"
```

#### Criar equipamento (POST)
```bash
curl -X POST "https://SEU_SITE.azurestaticapps.net/data-api/rest/Equipamento" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "nome": "Teste API",
    "potencia": 1.5,
    "horas_uso": 8.0,
    "categoria": "Teste"
  }'
```

## 🚨 Troubleshooting

### Erro 400 - Bad Request
- ✅ Verificar formato da connection string
- ✅ Verificar se todas as variáveis estão configuradas
- ✅ Validar JSON do request (para POST)

### Erro 500 - Internal Server Error
- ✅ Verificar se o banco de dados está acessível
- ✅ Verificar credenciais da connection string
- ✅ Verificar se a tabela `dbo.equipamentos` existe
- ✅ Verificar logs do Azure Static Web Apps

### Erro de Autenticação
- ✅ Verificar configuração AAD no Azure
- ✅ Verificar se o usuário tem acesso ao Static Web App
- ✅ Testar endpoint `/.auth/me`

### Erro de CORS
- ✅ Verificar origem no arquivo DAB config
- ✅ Atualizar `origins` para incluir seu domínio

## 📝 Checklist de Configuração

- [ ] Connection string no formato SQL Server (não SQLAlchemy)
- [ ] Variável `DATABASE_CONNECTION_STRING` configurada no Azure
- [ ] Tabela `dbo.equipamentos` criada no banco
- [ ] Permissões do banco configuradas
- [ ] CORS configurado para seu domínio
- [ ] Autenticação AAD funcionando
- [ ] Deploy realizado após configuração

## 🔗 Links Úteis

- [Azure Static Web Apps Data API Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/database-overview)
- [SQL Server Connection Strings](https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/connection-string-syntax)
- [Azure SQL Database Connectivity](https://docs.microsoft.com/en-us/azure/azure-sql/database/connect-query-overview)