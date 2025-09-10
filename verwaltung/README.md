# Configuração do Banco de Dados - SmartSpaar

Este diretório contém os arquivos de configuração do banco de dados para o sistema SmartSpaar.

## Arquivo: init_db.sql

Script SQL para criar as tabelas necessárias no banco Azure SQL Database (`smartspaar.database.windows.net`).

### Tabelas Criadas:

1. **Users** - Usuários do sistema
2. **ClientRecord** - Registros de clientes
3. **Equipamento** - Equipamentos do dashboard (NOVA TABELA)

### Como executar:

1. Conecte-se ao banco `smartspaar.database.windows.net`
2. Execute o script `init_db.sql` no banco `main`

```sql
-- Conectar ao banco
USE main;

-- Executar o script
-- (copie e cole o conteúdo de init_db.sql)
```

## Estrutura da Tabela Equipamento

A tabela `Equipamento` foi criada para suportar todas as funcionalidades do dashboard:

- **id**: Chave primária auto-incremento
- **nome**: Nome do equipamento (obrigatório)
- **potencia**: Potência em kW (obrigatório)
- **horas_uso**: Horas de uso diário (obrigatório)
- **categoria**: Categoria do equipamento (opcional)
- **idade**: Idade em anos (opcional)
- **etiqueta_eficiencia**: Etiqueta de eficiência energética (opcional)
- **observacoes**: Observações gerais (opcional)
- **tag**: Tag/identificador interno (opcional)
- **fator_correcao**: Fator de correção para cálculos (padrão: 1.00)
- **op_hora_ini**: Horário de início de operação (opcional)
- **op_hora_fim**: Horário de fim de operação (opcional)
- **connected_to**: Conexão com sites/unidades (opcional)
- **created_at**: Data de criação (automático)
- **updated_at**: Data de atualização (automático)

## Configuração no Azure

### 1. Azure Static Web Apps

O arquivo `database.config.json` configura o Data API Builder para conectar com o Azure SQL Database.

### 2. Variáveis de Ambiente

Configure a variável `DATABASE_CONNECTION_STRING` no Azure Static Web Apps:

```
DATABASE_CONNECTION_STRING=Server=smartspaar.database.windows.net;Database=main;User ID=seu_usuario;Password=sua_senha;Trusted_Connection=False;Connection Timeout=30;Encrypt=True;
```

### 3. Permissões

- O Data API requer autenticação para todas as operações
- Usuários autenticados podem criar, ler, atualizar e deletar equipamentos
- A autenticação é gerenciada pelo Azure Static Web Apps

## Testando a Configuração

Após a configuração:

1. Acesse `/dashboard` (requer autenticação)
2. Teste o carregamento da lista de equipamentos
3. Teste a adição de novos equipamentos via `/dashboard/adicionar_equipamento.html`

## Endpoints da API

- GET `/data-api/rest/Equipamento` - Listar equipamentos
- POST `/data-api/rest/Equipamento` - Criar equipamento
- PUT `/data-api/rest/Equipamento/{id}` - Atualizar equipamento
- DELETE `/data-api/rest/Equipamento/{id}` - Deletar equipamento