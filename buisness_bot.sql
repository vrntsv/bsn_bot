-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               10.3.13-MariaDB - mariadb.org binary distribution
-- Операционная система:         Win64
-- HeidiSQL Версия:              10.1.0.5464
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Дамп структуры для таблица buisnes_bot.admins
CREATE TABLE IF NOT EXISTS `admins` (
  `id` bigint(20) NOT NULL,
  `date_registr` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'Дата регистрации',
  `max_employees` int(20) NOT NULL DEFAULT 0 COMMENT 'Кол-во работников',
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Наличие активной подписки',
  `promo` varchar(50) DEFAULT NULL COMMENT 'Акционный промокод',
  `balance` mediumint(9) DEFAULT 0,
  `bonuses` mediumint(9) DEFAULT 0,
  `tarif` mediumint(9) DEFAULT 0 COMMENT 'руб/день',
  `id_referal` bigint(20) DEFAULT NULL COMMENT 'id реферала',
  `trial` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы buisnes_bot.admins: ~3 rows (приблизительно)
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` (`id`, `date_registr`, `max_employees`, `status`, `promo`, `balance`, `bonuses`, `tarif`, `id_referal`, `trial`) VALUES
	(171761490, '2020-03-19 20:16:35', 0, 0, NULL, 0, 0, 0, NULL, NULL),
	(332729470, '2020-03-20 21:31:14', 0, 0, NULL, 0, 0, 0, NULL, NULL),
	(758184015, '2020-03-19 22:37:50', 0, 0, NULL, 0, 0, 0, NULL, NULL);
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;

-- Дамп структуры для таблица buisnes_bot.company_list
CREATE TABLE IF NOT EXISTS `company_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_admin` bigint(20) NOT NULL,
  `name_company` varchar(255) NOT NULL,
  UNIQUE KEY `id` (`id`),
  KEY `FK_company_list_admins` (`id_admin`),
  CONSTRAINT `FK_company_list_admins` FOREIGN KEY (`id_admin`) REFERENCES `admins` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы buisnes_bot.company_list: ~6 rows (приблизительно)
/*!40000 ALTER TABLE `company_list` DISABLE KEYS */;
INSERT INTO `company_list` (`id`, `id_admin`, `name_company`) VALUES
	(2, 758184015, 'Первый созданный проект'),
	(3, 758184015, 'Второй созданный проект'),
	(4, 758184015, 'Финальный тест проектища'),
	(5, 758184015, 'Еще один проектище'),
	(6, 758184015, 'Финааал'),
	(7, 332729470, 'Тест');
/*!40000 ALTER TABLE `company_list` ENABLE KEYS */;

-- Дамп структуры для таблица buisnes_bot.employees
CREATE TABLE IF NOT EXISTS `employees` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(250) DEFAULT NULL,
  `id_company` int(11) DEFAULT NULL,
  `date_reg` datetime NOT NULL DEFAULT current_timestamp(),
  `fine` int(25) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_user` (`id`),
  KEY `FK_employees_company_list` (`id_company`),
  CONSTRAINT `FK_employees_company_list` FOREIGN KEY (`id_company`) REFERENCES `company_list` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы buisnes_bot.employees: ~6 rows (приблизительно)
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` (`id`, `full_name`, `id_company`, `date_reg`, `fine`) VALUES
	(111, 'Романов Роман', 5, '2020-03-19 15:22:12', 230),
	(222, 'Алексей Куркурыч', NULL, '2020-03-19 15:22:24', 500),
	(11213123, NULL, 6, '2020-03-21 02:38:07', 0),
	(115135132132, NULL, NULL, '2020-03-21 02:38:44', 0),
	(213124124124124, NULL, NULL, '2020-03-21 02:36:52', 0),
	(1223124124124124124, NULL, NULL, '2020-03-21 02:34:42', 0);
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;

-- Дамп структуры для таблица buisnes_bot.questions_list
CREATE TABLE IF NOT EXISTS `questions_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_template` int(11) NOT NULL,
  `id_company` int(11) NOT NULL,
  `id_user` bigint(20) NOT NULL,
  `text_question` varchar(4096) NOT NULL,
  `text_answer` varchar(4096) DEFAULT NULL,
  `time_to_answer` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `FK_questions_list_users` (`id_user`),
  KEY `FK_questions_list_company_list` (`id_company`),
  KEY `FK_questions_list_questions_template` (`id_template`),
  CONSTRAINT `FK_questions_list_company_list` FOREIGN KEY (`id_company`) REFERENCES `company_list` (`id`),
  CONSTRAINT `FK_questions_list_questions_template` FOREIGN KEY (`id_template`) REFERENCES `questions_template` (`id`),
  CONSTRAINT `FK_questions_list_users` FOREIGN KEY (`id_user`) REFERENCES `admins` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы buisnes_bot.questions_list: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `questions_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `questions_list` ENABLE KEYS */;

-- Дамп структуры для таблица buisnes_bot.questions_template
CREATE TABLE IF NOT EXISTS `questions_template` (
  `id` int(11) NOT NULL DEFAULT 0,
  `id_company` int(11) NOT NULL,
  `text` varchar(4096) NOT NULL,
  `id_user` bigint(20) NOT NULL,
  `time_to_send` time NOT NULL DEFAULT '20:00:00',
  `timer_to_answer` time NOT NULL DEFAULT '04:00:00',
  `monday` tinyint(1) DEFAULT 0,
  `tuesday` tinyint(1) DEFAULT 0,
  `wednsday` tinyint(1) DEFAULT 0,
  `thursday` tinyint(1) unsigned DEFAULT 0,
  `friday` tinyint(1) DEFAULT 0,
  `saturday` tinyint(1) DEFAULT 0,
  `sunday` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `FK_questions_template_company_list` (`id_company`),
  KEY `FK_questions_template_employees` (`id_user`),
  CONSTRAINT `FK_questions_template_company_list` FOREIGN KEY (`id_company`) REFERENCES `company_list` (`id`),
  CONSTRAINT `FK_questions_template_employees` FOREIGN KEY (`id_user`) REFERENCES `employees` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы buisnes_bot.questions_template: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `questions_template` DISABLE KEYS */;
/*!40000 ALTER TABLE `questions_template` ENABLE KEYS */;

-- Дамп структуры для таблица buisnes_bot.reports
CREATE TABLE IF NOT EXISTS `reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_company` int(11) NOT NULL,
  `id_user` bigint(20) NOT NULL,
  `status` tinyint(1) DEFAULT 0,
  `id_question` int(11) DEFAULT NULL,
  `answer` int(11) DEFAULT NULL,
  `date_send` datetime NOT NULL DEFAULT current_timestamp(),
  `date_answer` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `FK_reports_company_list` (`id_company`),
  KEY `FK_reports_users` (`id_user`),
  KEY `FK_reports_questions_list` (`id_question`),
  CONSTRAINT `FK_reports_company_list` FOREIGN KEY (`id_company`) REFERENCES `company_list` (`id`),
  CONSTRAINT `FK_reports_questions_list` FOREIGN KEY (`id_question`) REFERENCES `questions_list` (`id`),
  CONSTRAINT `FK_reports_users` FOREIGN KEY (`id_user`) REFERENCES `admins` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы buisnes_bot.reports: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
