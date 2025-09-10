# LandingSeiteTEST
Das ist ein Test für unsere erste öffentliche Seite

## 🚀 Configuração da API de Dados (DAB - Data Access Builder)

Este projeto agora inclui configuração completa para Azure Static Web Apps com Data API Builder para conexão com SQL Server.

### 📋 Arquivos de Configuração

- `.env.example` - Template das variáveis de ambiente (configure `DATABASE_CONNECTION_STRING`)
- `swa-db-connections/staticwebapp.database.config.json` - Configuração do DAB
- `setup_database.sql` - Script para criar a tabela de equipamentos
- `DAB_CONFIGURATION_GUIDE.md` - Guia completo de configuração
- `test_dab_api.sh` - Script para testar a API

### 🛠️ Setup Rápido

1. **Configure a connection string:**
   ```bash
   cp .env.example .env
   # Edite .env com suas credenciais do Azure SQL
   ```

2. **Execute o script de setup do banco:**
   ```sql
   -- Execute setup_database.sql no seu Azure SQL Database
   ```

3. **Teste a API:**
   ```bash
   chmod +x test_dab_api.sh
   ./test_dab_api.sh https://seu-site.azurestaticapps.net
   ```

### 📖 Documentação Completa

Consulte `DAB_CONFIGURATION_GUIDE.md` para instruções detalhadas de configuração, troubleshooting e exemplos de uso.

### 🧪 Dashboard de Diagnóstico

Acesse `/dashboard/diagnostico_avancado.html` para testar a conectividade e funcionalidade da API em tempo real.
