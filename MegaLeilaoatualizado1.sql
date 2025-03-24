-- Criação do banco de dados
drop database megaleilao1;
CREATE DATABASE megaleilao1;
USE megaleilao1;

-- Tabela de usuários com cpf e email
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    cpf VARCHAR(14) NOT NULL UNIQUE, -- Formato típico: "123.456.789-00"
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

-- Tabela de veículos
CREATE TABLE veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(15, 2) NOT NULL,
    descricao TEXT,
    imagem_caminho VARCHAR(255),
    status ENUM('disponivel', 'vendido') DEFAULT 'disponivel',
    buyer_id INT,
    FOREIGN KEY (buyer_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Índices para melhorar performance
CREATE INDEX idx_status ON veiculos(status);
CREATE INDEX idx_buyer_id ON veiculos(buyer_id);

-- Dados de teste (opcional)
INSERT INTO usuarios (nome, cpf, email, senha) 
VALUES ('teste', '123.456.789-00', 'teste@example.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');

INSERT INTO veiculos (nome, preco, descricao, imagem_caminho) 
VALUES ('Fusca 1970', 15000.00, 'Carro clássico em bom estado', 'images/fusca.jpg');

select * from veiculos

