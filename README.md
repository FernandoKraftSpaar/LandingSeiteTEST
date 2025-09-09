# SmartSpaar Landing Page

Landing page da SmartSpaar com dashboard integrado via Azure Data API Builder (DAB).

## 🚀 Configuração Rápida

### 1. Configurar Banco de Dados

1. Execute o script `setup_database.sql` no seu Azure SQL Database
2. Configure a connection string no formato correto

### 2. Configurar Variáveis de Ambiente

**Azure Static Web Apps (Produção):**
```
DATABASE_CONNECTION_STRING=Server=seu_servidor.database.windows.net,1433;Database=seu_banco;User Id=seu_usuario;Password=sua_senha;Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;
```

**Local (.env):**
Copie `.env.example` para `.env` e configure com seus dados reais.

### 3. Testar a API

Execute o script de teste:
```bash
./test_dab_api.sh https://seu-site.azurestaticapps.net
```

## 🔧 Troubleshooting

- **Erro 400/500**: Consulte `DAB_CONFIGURATION_GUIDE.md` para solução completa
- **Connection String**: Use formato SQL Server, não SQLAlchemy
- **Autenticação**: Configure Azure AD no Static Web Apps

## 📁 Estrutura

- `/dashboard/` - Interface do dashboard
- `/swa-db-connections/` - Configuração DAB
- `DAB_CONFIGURATION_GUIDE.md` - Guia completo de configuração
- `setup_database.sql` - Script de setup do banco
- `test_dab_api.sh` - Script de teste da API
Das ist ein Test für unsere erste öffentliche Seite
