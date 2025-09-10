-- SQL schema minimal (para Azure SQL ou outro)
CREATE TABLE [Users] (
  [id] INT IDENTITY(1,1) PRIMARY KEY,
  [username] NVARCHAR(80) NOT NULL UNIQUE,
  [email] NVARCHAR(200) NOT NULL UNIQUE,
  [password_hash] NVARCHAR(200) NOT NULL,
  [role] NVARCHAR(50) DEFAULT 'operator'
);

CREATE TABLE [ClientRecord] (
  [id] INT IDENTITY(1,1) PRIMARY KEY,
  [name] NVARCHAR(200),
  [source] NVARCHAR(100),
  [active] BIT DEFAULT 1,
  [last_seen] DATETIME2 DEFAULT GETUTCDATE()
);

-- Tabela de equipamentos para o dashboard SmartSpaar
CREATE TABLE [Equipamento] (
  [id] INT IDENTITY(1,1) PRIMARY KEY,
  [nome] NVARCHAR(200) NOT NULL,
  [potencia] DECIMAL(10,2) NOT NULL,
  [horas_uso] DECIMAL(5,2) NOT NULL,
  [categoria] NVARCHAR(100),
  [idade] INT,
  [etiqueta_eficiencia] NVARCHAR(50),
  [observacoes] NVARCHAR(MAX),
  [tag] NVARCHAR(100),
  [fator_correcao] DECIMAL(5,2) DEFAULT 1.00,
  [op_hora_ini] TIME,
  [op_hora_fim] TIME,
  [connected_to] NVARCHAR(100),
  [created_at] DATETIME2 DEFAULT GETUTCDATE(),
  [updated_at] DATETIME2 DEFAULT GETUTCDATE()
);
