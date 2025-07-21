-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 21/07/2025 às 20:36
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
-- Estrutura para tabela `comparacao_diaria_04`
--

CREATE TABLE `comparacao_diaria_04` (
  `A04_id` int(11) NOT NULL,
  `A04_codigo_barras` varchar(255) NOT NULL,
  `A04_nota_fiscal` varchar(255) NOT NULL,
  `A04_data` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `A04_situacao` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `comparacao_diaria_04`
--

INSERT INTO `comparacao_diaria_04` (`A04_id`, `A04_codigo_barras`, `A04_nota_fiscal`, `A04_data`, `A04_situacao`) VALUES
(1, '45149068888', '93211', '2025-07-21 13:55:11', ''),
(2, '45149067777', '93277', '2025-07-21 13:55:11', ''),
(3, '45149061470', '93232', '2025-07-21 13:55:11', ''),
(4, '45149060987', '93245', '2025-07-21 14:11:25', ''),
(5, '45149060999', '93299', '2025-07-21 14:35:30', ''),
(6, '45149060000', '93000', '2025-07-21 14:45:05', ''),
(7, '45149064444', '93444', '2025-07-21 15:19:23', ''),
(8, '45149063333', '93333', '2025-07-21 15:32:40', '');

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
(40, '13', '2025-07-13 21:44:30', 1),
(41, '45147174159', '2025-07-13 21:44:42', 1),
(46, '45077184517', '2025-07-13 21:45:08', 1),
(47, '45102720614', '2025-07-13 21:45:13', 1),
(48, '`^id^Ç^45102720614^,^t^Ç^lm^{', '2025-07-13 21:45:16', 1),
(49, '`^id^Ç^45077184517^,^t^Ç^lm^,^tn^Ç^888000999608968^{', '2025-07-13 21:45:19', 1),
(51, '45147239825', '2025-07-13 21:47:24', 1),
(54, '45147615072', '2025-07-13 21:47:35', 1),
(59, '509700719', '2025-07-14 10:01:52', 1),
(68, '`^id^Ç^45152050762^,^sender_id^Ç791883096,^hash_code^Ç^gbotsG4Pomr3r68cK;SXZwAMAZvucJd5p1GJ7FrAd6U=^,^security_digit^Ç^0^{', '2025-07-14 10:04:28', 1),
(74, '45066343702', '2025-07-14 10:15:32', 1),
(87, '888000999608968', '2025-07-14 10:34:34', 1),
(88, 'idÇ45150847847,^sender_id^Ç791883096,^hash_codeÇm5o9f1feYSm;UbAvLZ;w;CjIVoP){E2dEjdDR5omh0=^,^security_digit^Ç^0^{', '2025-07-15 21:20:47', 1),
(92, '45149061470', '2025-07-16 23:20:27', 1),
(97, '1333', '2025-07-17 17:43:18', NULL),
(98, '1345', '2025-07-17 17:43:22', NULL),
(103, '45149067777', '2025-07-17 18:13:27', 4),
(106, '45149068888', '2025-07-18 17:23:22', 7),
(126, '45149060987', '2025-07-21 14:14:58', 27),
(127, '45149060999', '2025-07-21 14:38:20', 29),
(130, '45149060000', '2025-07-21 15:10:08', 36),
(131, '45149064444', '2025-07-21 15:19:53', 37),
(132, '45149064444', '2025-07-21 15:35:09', 37);

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
(1, 1, '93232', '2025-07-13 20:02:16'),
(2, 1, 'TEMP', '2025-07-17 18:06:28'),
(3, 1, 'TEMP', '2025-07-17 18:07:44'),
(4, 1, '93277', '2025-07-17 18:13:27'),
(5, 1, 'TEMP', '2025-07-18 13:22:52'),
(6, 1, 'TEMP', '2025-07-18 17:11:46'),
(7, 1, '93211', '2025-07-18 17:23:22'),
(8, 1, 'TEMP', '2025-07-20 20:38:14'),
(9, 1, 'TEMP', '2025-07-20 20:39:13'),
(10, 1, 'TEMP', '2025-07-20 20:41:22'),
(11, 1, 'TEMP', '2025-07-20 20:47:31'),
(12, 1, 'TEMP', '2025-07-20 21:03:41'),
(13, 1, 'TEMP', '2025-07-20 21:03:48'),
(14, 1, 'TEMP', '2025-07-20 21:10:18'),
(15, 1, 'TEMP', '2025-07-20 21:10:24'),
(16, 1, 'TEMP', '2025-07-20 21:10:29'),
(17, 1, 'TEMP', '2025-07-20 21:12:18'),
(18, 1, 'TEMP', '2025-07-20 21:16:09'),
(19, 1, 'TEMP', '2025-07-20 21:16:18'),
(20, 1, 'TEMP', '2025-07-20 21:16:35'),
(21, 1, 'TEMP', '2025-07-20 21:16:37'),
(22, 1, 'TEMP', '2025-07-20 21:16:37'),
(23, 1, 'TEMP', '2025-07-20 21:16:38'),
(24, 1, 'TEMP', '2025-07-20 21:16:39'),
(25, 1, 'TEMP', '2025-07-20 21:16:40'),
(26, 1, 'TEMP', '2025-07-20 21:16:40'),
(27, 1, 'TEMP', '2025-07-21 14:14:58'),
(29, 1, 'TEMP', '2025-07-21 14:38:20'),
(36, 1, '93000', '2025-07-21 15:10:08'),
(37, 1, '93444', '2025-07-21 15:19:53');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `comparacao_diaria_04`
--
ALTER TABLE `comparacao_diaria_04`
  ADD PRIMARY KEY (`A04_id`);

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
-- AUTO_INCREMENT de tabela `comparacao_diaria_04`
--
ALTER TABLE `comparacao_diaria_04`
  MODIFY `A04_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `empresa_03`
--
ALTER TABLE `empresa_03`
  MODIFY `A03_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `etiqueta_02`
--
ALTER TABLE `etiqueta_02`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=133;

--
-- AUTO_INCREMENT de tabela `notafiscal_01`
--
ALTER TABLE `notafiscal_01`
  MODIFY `A01_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

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
