CREATE TABLE `NAME` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `USERNAME` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `LAST_VISIT` int(10) unsigned DEFAULT NULL,
  `LINK_ID` int(10) unsigned NOT NULL,
  `ADD_TIME` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `LINK_ID` (`LINK_ID`),
  `SEX` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `HOMETOWN` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM AUTO_INCREMENT=49486 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

