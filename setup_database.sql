-- Script SQL para criar a tabela de equipamentos
-- Execute este script no seu Azure SQL Database

-- Criar tabela se não existir
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='equipamentos' AND xtype='U')
BEGIN
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
    
    PRINT 'Tabela equipamentos criada com sucesso!';
END
ELSE
BEGIN
    PRINT 'Tabela equipamentos já existe.';
END

-- Criar índices para melhor performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_equipamentos_categoria')
BEGIN
    CREATE INDEX IX_equipamentos_categoria ON dbo.equipamentos(categoria);
    PRINT 'Índice IX_equipamentos_categoria criado.';
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_equipamentos_tag')
BEGIN
    CREATE INDEX IX_equipamentos_tag ON dbo.equipamentos(tag);
    PRINT 'Índice IX_equipamentos_tag criado.';
END

-- Trigger para atualizar updated_at automaticamente
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'tr_equipamentos_updated_at')
BEGIN
    EXEC('
    CREATE TRIGGER tr_equipamentos_updated_at
    ON dbo.equipamentos
    AFTER UPDATE
    AS
    BEGIN
        SET NOCOUNT ON;
        UPDATE dbo.equipamentos 
        SET updated_at = GETDATE()
        FROM dbo.equipamentos e
        INNER JOIN inserted i ON e.id = i.id;
    END
    ');
    PRINT 'Trigger tr_equipamentos_updated_at criado.';
END

-- Inserir dados de exemplo (opcional)
IF NOT EXISTS (SELECT TOP 1 * FROM dbo.equipamentos)
BEGIN
    INSERT INTO dbo.equipamentos (nome, potencia, horas_uso, categoria, idade, etiqueta_eficiencia, observacoes, tag)
    VALUES 
        ('Compressor Principal', 15.5, 8.0, 'Refrigeração', 3, 'IE3', 'Equipamento principal da linha de produção', 'COMP-001'),
        ('Motor Bomba d''Água', 3.2, 12.0, 'Motorização', 2, 'IE2', 'Sistema de circulação de água', 'MOTOR-002'),
        ('Iluminação LED Galpão', 2.1, 10.0, 'Iluminação', 1, 'A++', 'Iluminação principal do galpão', 'LED-003'),
        ('Forno Industrial', 25.0, 6.0, 'Processo', 5, 'B', 'Forno para tratamento térmico', 'FORNO-004'),
        ('Ventilador Exaustor', 1.8, 16.0, 'Refrigeração', 4, 'IE1', 'Sistema de ventilação', 'VENT-005');
    
    PRINT 'Dados de exemplo inseridos!';
END

-- Verificar se tudo foi criado corretamente
SELECT 
    COUNT(*) as total_equipamentos,
    AVG(potencia) as potencia_media,
    SUM(potencia * horas_uso * 30) as consumo_mensal_estimado_kwh
FROM dbo.equipamentos;

PRINT 'Script executado com sucesso!';
PRINT 'Agora configure a CONNECTION_STRING no formato:';
PRINT 'Server=seu_servidor.database.windows.net,1433;Database=seu_banco;User Id=seu_usuario;Password=sua_senha;Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;';