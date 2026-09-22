-- AsuraCORE: new map 9000 "Святилище Асуры" (floating void island), terrain files are served by the launcher
-- WDT FileDataID 9100000 (see F:\AsuraCORE\tools\mapkit\make_island.py)

SET @MAP     := 9000;
SET @MAPDIFF := 90000;

DELETE FROM `map` WHERE `ID` = @MAP;
INSERT INTO `map` (`ID`, `Directory`, `MapName`, `MapDescription0`, `MapDescription1`, `PvpShortDescription`, `PvpLongDescription`, `CorpseX`, `CorpseY`, `MapType`, `InstanceType`, `ExpansionID`, `AreaTableID`, `LoadingScreenID`, `TimeOfDayOverride`, `ParentMapID`, `CosmeticParentMapID`, `TimeOffset`, `MinimapIconScale`, `CorpseMapID`, `MaxPlayers`, `WindSettingsID`, `ZmpFileDataID`, `WdtFileDataID`, `NavigationMaxDistance`, `PreloadFileDataID`, `Flags1`, `Flags2`, `Flags3`, `VerifiedBuild`) VALUES
(@MAP, 'AsuraSanctum', 'Святилище Асуры', '', '', '', '', 0, 0, 1, 0, 0, 0, 0, -1, -1, -1, 0, 1, -1, 0, 12, 0, 1440315, 0, 0, 142622301, 134479888, 0, 69875);

DELETE FROM `map_locale` WHERE `ID` = @MAP;
INSERT INTO `map_locale` (`ID`, `locale`, `MapName_lang`, `MapDescription0_lang`, `MapDescription1_lang`, `PvpShortDescription_lang`, `PvpLongDescription_lang`, `VerifiedBuild`) VALUES
(@MAP, 'ruRU', 'Святилище Асуры', '', '', '', '', 69875);

DELETE FROM `map_difficulty` WHERE `ID` = @MAPDIFF;
INSERT INTO `map_difficulty` (`Message`, `ID`, `DifficultyID`, `LockID`, `ResetInterval`, `MaxPlayers`, `ItemContext`, `ItemContextPickerID`, `Flags`, `ContentTuningID`, `WorldStateExpressionID`, `MapID`, `VerifiedBuild`) VALUES
('', @MAPDIFF, 0, 0, 0, 5, 0, 0, 0, 0, 0, @MAP, 69875);

-- hotfix push: 3179597154 = Map.db2, 2456155917 = MapDifficulty.db2 (TableHash from the DB2 headers)
DELETE FROM `hotfix_data` WHERE `Id` IN (900001, 900002);
INSERT INTO `hotfix_data` (`Id`, `UniqueId`, `TableHash`, `RecordId`, `Status`, `VerifiedBuild`) VALUES
(900002, 90000003, 3179597154, @MAP, 1, 69875),
(900002, 90000004, 2456155917, @MAPDIFF, 1, 69875);
