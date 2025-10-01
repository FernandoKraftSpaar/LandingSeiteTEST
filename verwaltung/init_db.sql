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

CREATE TABLE [PilotRegistrations] (
  [id] INT IDENTITY(1,1) PRIMARY KEY,
  [name] NVARCHAR(200) NOT NULL,
  [contact] NVARCHAR(200) NOT NULL,
  [industrial_branch] NVARCHAR(100),
  [telefone] NVARCHAR(50),
  [company] NVARCHAR(200),
  [challenge] NVARCHAR(MAX),
  [created_at] DATETIME2 DEFAULT GETUTCDATE(),
  [status] NVARCHAR(50) DEFAULT 'pending'
);
