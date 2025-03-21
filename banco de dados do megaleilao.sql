-- Criar o banco de dados
DROP DATABASE IF EXISTS megaleilao; -- Remove o banco antigo, se existir
CREATE DATABASE megaleilao;
USE megaleilao;

-- Criar tabela de usuários
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL
);

-- Criar tabela de veículos
CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    description TEXT,
    image_path VARCHAR(255),
    status ENUM('available', 'sold') DEFAULT 'available'
);

-- Criar tabela de favoritos
CREATE TABLE favorites (
    user_id VARCHAR(50),
    vehicle_id INT,
    PRIMARY KEY (user_id, vehicle_id),
    FOREIGN KEY (user_id) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

-- Inserir dados iniciais na tabela users
INSERT INTO users (username, password) VALUES
    ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'), -- senha: admin
    ('user1', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'), -- senha: password
    ('user2', 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb9'); -- senha: user123

-- Inserir dados iniciais na tabela vehicles
INSERT INTO vehicles (name, price, description, image_path, status) VALUES
    ('Audi A3', 190000.00, '1.4 35 TFSI GASOLINA SEDAN S LINE', 'audi-a3-velocidade.png', 'available'),
    ('BMW M5', 500000.00, 'High-performance sedan', 'bmw-m5-cs-10.png', 'available'),
    ('Fiat Uno', 30000.00, 'Carro econômico popular', 'fiat-uno.png', 'available');

-- Inserir um favorito de exemplo (opcional)
INSERT INTO favorites (user_id, vehicle_id) VALUES
    ('admin', 1); -- Admin favoritou o Audi A3
    
select * from users