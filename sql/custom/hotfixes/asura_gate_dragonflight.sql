-- AsuraCORE: the server runs Dragonflight content; The War Within and Midnight are closed.
-- Gating itself is done by worldserver.conf (Expansion = 9, MaxPlayerLevel = 70) and account.expansion.
-- Here we only lower the expansion requirement of maps we use for our own content.

-- Priory of the Sacred Flame (2649) hosts our Priory of the Void instance, so it must stay reachable.
DELETE FROM `map` WHERE `ID` = 2649;
INSERT INTO `map` (`ID`, `Directory`, `MapName`, `MapDescription0`, `MapDescription1`, `PvpShortDescription`, `PvpLongDescription`, `CorpseX`, `CorpseY`, `MapType`, `InstanceType`, `ExpansionID`, `AreaTableID`, `LoadingScreenID`, `TimeOfDayOverride`, `ParentMapID`, `CosmeticParentMapID`, `TimeOffset`, `MinimapIconScale`, `CorpseMapID`, `MaxPlayers`, `WindSettingsID`, `ZmpFileDataID`, `WdtFileDataID`, `NavigationMaxDistance`, `PreloadFileDataID`, `Flags1`, `Flags2`, `Flags3`, `VerifiedBuild`) VALUES
(2649, '2649', 'Приорат Пустоты', '', '', '', '', 0, 0, 1, 1, 0, 0, 624, -1, -1, 2601, 0, 1, -1, 0, 12, 0, 5206340, 0, 0, 143670877, 33808, 12, 69875);

DELETE FROM `map_locale` WHERE `ID` = 2649;
INSERT INTO `map_locale` (`ID`, `locale`, `MapName_lang`, `MapDescription0_lang`, `MapDescription1_lang`, `PvpShortDescription_lang`, `PvpLongDescription_lang`, `VerifiedBuild`) VALUES
(2649, 'ruRU', 'Приорат Пустоты', '', '', '', '', 69875);

DELETE FROM `hotfix_data` WHERE `Id` = 900003;
INSERT INTO `hotfix_data` (`Id`, `UniqueId`, `TableHash`, `RecordId`, `Status`, `VerifiedBuild`) VALUES
(900003, 90000005, 3179597154, 2649, 1, 69875);
