CREATE TABLE `weather_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `longitude` varchar(20) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `city` varchar(80) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL COMMENT 'GEN DESC OF WEATHER',
  `temperature` float(5,2) DEFAULT NULL,
  `temperature_min` float(5,2) DEFAULT NULL,
  `temperature_max` float(5,2) DEFAULT NULL,
  `humidity` float(5,2) DEFAULT NULL,
  `wind` float(5,2) DEFAULT NULL,
  `sunrise` int(8) DEFAULT NULL COMMENT 'unixtimestamp',
  `sunset` int(8) DEFAULT NULL COMMENT 'unixtimestamp',
  `current_output` float(5,2) DEFAULT NULL,
  `current_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `status` binary(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8