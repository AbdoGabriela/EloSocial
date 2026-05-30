CREATE DATABASE IF NOT EXISTS 02_EloSocial;
USE 02_EloSocial;

-- Tabela 01 - Estabelecimento - Tabela ADM (Não irá aparecer em Python)
CREATE TABLE IF NOT EXISTS tbl_estabelecimento (
    id_esta INT AUTO_INCREMENT PRIMARY KEY,
    nome_esta VARCHAR(100) NOT NULL,
    tipo_esta VARCHAR(100) -- ex: Casa de Acolhimento, UBS, Clínica, Hospital
);

-- Tabela 02 - Medicação
CREATE TABLE IF NOT EXISTS tbl_medicacao (
	id_med INT AUTO_INCREMENT PRIMARY KEY,
    ean VARCHAR(13) NOT NULL UNIQUE, -- "Código de Barras"
    nome_med VARCHAR(100) NOT NULL -- Nome do medicamento COM dosagem
);

-- Tabela 03 - Acolhido
CREATE TABLE IF NOT EXISTS tbl_acolhido (
    id_acolhido INT AUTO_INCREMENT PRIMARY KEY,
    nome_acolhido VARCHAR(100) NOT NULL, 
    cpf CHAR(11) NOT NULL UNIQUE,
    data_nasc DATE NOT NULL,
    cid VARCHAR(100),
    fk_nome_esta INT NOT NULL,
    CONSTRAINT FOREIGN KEY (fk_nome_esta) REFERENCES tbl_estabelecimento (id_esta)
);

-- Tabela 04 - Consulta
CREATE TABLE IF NOT EXISTS tbl_consulta_exame (
	id_cons INT AUTO_INCREMENT PRIMARY KEY,
    fk_acolhido INT NOT NULL,
    fk_nome_esta INT,
	data_cons DATE NOT NULL,
    hora_cons TIME NOT NULL,
    tipo_cons VARCHAR(100),
	CONSTRAINT FOREIGN KEY (fk_nome_esta) REFERENCES tbl_estabelecimento (id_esta) ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (fk_acolhido) REFERENCES tbl_acolhido (id_acolhido) ON DELETE CASCADE
    
);
    
-- Tabela 05 - relacionamento acolhido e medicação
CREATE TABLE IF NOT EXISTS tbl_acolhido_medicacao (
    id_acol_med INT AUTO_INCREMENT PRIMARY KEY,
    fk_acolhido INT NOT NULL,
    fk_med INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE, -- NULL = uso contínuo
    frequencia VARCHAR(50),-- ex: "2x ao dia"
    observacao VARCHAR(255),
    CONSTRAINT FOREIGN KEY (fk_acolhido) REFERENCES tbl_acolhido (id_acolhido) ON DELETE CASCADE,
	CONSTRAINT FOREIGN KEY (fk_med) REFERENCES tbl_medicacao (id_med) ON DELETE CASCADE
);



-- Inserção de Estabelecimentos.
/* INSERT INTO tbl_estabelecimento (nome_esta, tipo_esta) VALUES 
('Residência Inclusiva', 'Residência de Acolhimento'), 
('SAICA', 'Residência de Acolhimento'), 
('Centro Provisório de Acolhimento', 'Residência de Acolhimento'),
('UBS Oliveira Marabá', 'UBS'), 
('Clínica Uchida', 'Clínica'), 
('AME', 'Centro Público de Saúde');*/

-- Inserção de Acolhidos.
/*INSERT INTO tbl_acolhido (nome_acolhido,cpf,data_nasc,cid,fk_nome_esta) VALUES
('João das Neves', '12345678923', '2000-01-01', 'CID 10 F 31', 1),
('Clementina de Jesus', '11122233344', '2000-02-02', null, 1),
('Michael Jackson da Silva', '99988877744', '1958-08-29', 'CID 10 L80 M32', 1);*/

-- Inserção de Medicamentos.
/*INSERT INTO tbl_medicacao (ean, nome_med) VALUES
('7896004716176', 'Hidroclorotizida 25mg EMS'),
('7896714208565', 'Losartana 50mg Neo Química'),
('7896422514651', 'Clonazepam 2 mg Medley');*/