-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 14/07/2025 às 02:41
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `db_click`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `empresa_03`
--

CREATE TABLE `empresa_03` (
  `A03_id` int(11) NOT NULL,
  `A03_nome` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `empresa_03`
--

INSERT INTO `empresa_03` (`A03_id`, `A03_nome`) VALUES
(1, 'Empresa Exemplo');

-- --------------------------------------------------------

--
-- Estrutura para tabela `etiqueta_02`
--

CREATE TABLE `etiqueta_02` (
  `id` int(11) NOT NULL,
  `codigo` varchar(255) NOT NULL,
  `A02_data` datetime DEFAULT NULL,
  `Notafiscal_01_A01_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `etiqueta_02`
--

INSERT INTO `etiqueta_02` (`id`, `codigo`, `A02_data`, `Notafiscal_01_A01_id`) VALUES
(1, '45', '2025-07-13 20:06:32', 1),
(2, '65', '2025-07-13 20:07:20', 1),
(3, '67', '2025-07-13 20:07:30', 1),
(8, '44', '2025-07-13 20:17:52', 1),
(10, '55', '2025-07-13 20:22:05', 1),
(14, '89', '2025-07-13 20:22:50', 1),
(15, '5', '2025-07-13 20:24:52', 1),
(24, '88', '2025-07-13 21:15:26', 1),
(25, '9', '2025-07-13 21:15:27', 1),
(26, '0', '2025-07-13 21:15:28', 1),
(27, '15', '2025-07-13 21:20:48', 1),
(33, '1', '2025-07-13 21:32:11', 1),
(34, '2', '2025-07-13 21:32:12', 1),
(35, '3', '2025-07-13 21:32:12', 1),
(36, '123', '2025-07-13 21:32:13', 1),
(37, '1234', '2025-07-13 21:32:15', 1),
(38, '12345', '2025-07-13 21:32:16', 1),
(39, '45', '2025-07-13 21:40:58', 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `notafiscal_01`
--

CREATE TABLE `notafiscal_01` (
  `A01_id` int(11) NOT NULL,
  `Empresa_03_A03_id` int(11) NOT NULL,
  `A01_codigo` varchar(255) DEFAULT NULL,
  `A01_data` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `notafiscal_01`
--

INSERT INTO `notafiscal_01` (`A01_id`, `Empresa_03_A03_id`, `A01_codigo`, `A01_data`) VALUES
(1, 1, 'NF001', '2025-07-13 20:02:16');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `empresa_03`
--
ALTER TABLE `empresa_03`
  ADD PRIMARY KEY (`A03_id`);

--
-- Índices de tabela `etiqueta_02`
--
ALTER TABLE `etiqueta_02`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Notafiscal_01_A01_id` (`Notafiscal_01_A01_id`);

--
-- Índices de tabela `notafiscal_01`
--
ALTER TABLE `notafiscal_01`
  ADD PRIMARY KEY (`A01_id`),
  ADD KEY `Empresa_03_A03_id` (`Empresa_03_A03_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `empresa_03`
--
ALTER TABLE `empresa_03`
  MODIFY `A03_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `etiqueta_02`
--
ALTER TABLE `etiqueta_02`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `etiqueta_02`
--
ALTER TABLE `etiqueta_02`
  ADD CONSTRAINT `etiqueta_02_ibfk_1` FOREIGN KEY (`Notafiscal_01_A01_id`) REFERENCES `notafiscal_01` (`A01_id`);

--
-- Restrições para tabelas `notafiscal_01`
--
ALTER TABLE `notafiscal_01`
  ADD CONSTRAINT `notafiscal_01_ibfk_1` FOREIGN KEY (`Empresa_03_A03_id`) REFERENCES `empresa_03` (`A03_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
