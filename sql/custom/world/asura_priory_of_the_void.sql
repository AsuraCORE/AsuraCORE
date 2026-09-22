-- AsuraCORE: Asura Sanctum hub (own map 9000) + Priory of the Void (map 2649) + boss Nal'Azur
-- Custom ID range: 900000+

SET @BOSS   := 900000;
SET @ADD    := 900001;
SET @PORTAL := 900000;
SET @CGUID  := 12000000;
SET @OGUID  := 12000000;

-- Creatures
DELETE FROM `creature_template` WHERE `entry` IN (@BOSS, @ADD);
INSERT INTO `creature_template` (`entry`, `name`, `subname`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `scale`, `Classification`, `dmgschool`, `BaseAttackTime`, `RangeAttackTime`, `BaseVariance`, `RangeVariance`, `unit_class`, `unit_flags`, `unit_flags2`, `unit_flags3`, `family`, `trainer_class`, `type`, `VehicleId`, `AIName`, `MovementType`, `ExperienceModifier`, `RacialLeader`, `movementId`, `WidgetSetID`, `WidgetSetUnitConditionID`, `RegenHealth`, `CreatureImmunitiesId`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
(@BOSS, 'Нал''Азур', 'Страж Пустоты', 16, 0, 1, 1.14286, 1.6, 1, 5, 2000, 2000, 1, 1, 8, 0, 0, 0, 0, 0, 3, 0, '', 0, 1, 0, 0, 0, 0, 1, 0, 1, 'boss_nalazur', 0),
(@ADD,  'Порождение Пустоты', '', 16, 0, 1, 1.14286, 1, 0, 5, 2000, 2000, 1, 1, 1, 0, 0, 0, 0, 0, 3, 0, '', 0, 1, 0, 0, 0, 0, 1, 0, 0, '', 0);

DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@BOSS, @ADD);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@BOSS, 0, 26214, 1, 1, 0), -- Void Lord
(@ADD,  0, 19368, 1, 1, 0); -- Void Terror

-- ContentTuning 2976 = Priory of the Sacred Flame trash, scales with the player
DELETE FROM `creature_template_difficulty` WHERE `Entry` IN (@BOSS, @ADD);
INSERT INTO `creature_template_difficulty` (`Entry`, `DifficultyID`, `ContentTuningID`, `HealthScalingExpansion`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `DamageModifier`, `TypeFlags`) VALUES
(@BOSS, 0, 2976, 10, 30, 1, 1, 3, 4), -- TypeFlags 4 = boss
(@BOSS, 1, 2976, 10, 30, 1, 1, 3, 4),
(@ADD,  0, 2976, 10, 1.5, 1, 1, 1, 0),
(@ADD,  1, 2976, 10, 1.5, 1, 1, 1, 0);

-- Two-way Void Portal (goober -> go_asura_void_portal)
DELETE FROM `gameobject_template` WHERE `entry` = @PORTAL;
INSERT INTO `gameobject_template` (`entry`, `type`, `displayId`, `name`, `IconName`, `castBarCaption`, `unk1`, `size`, `ContentTuningId`, `RequiredLevel`, `AIName`, `ScriptName`, `VerifiedBuild`) VALUES
(@PORTAL, 10, 94774, 'Портал Пустоты', '', '', '', 1.2, 0, 0, '', 'go_asura_void_portal', 0);

-- Instance: Priory of the Sacred Flame map reused with our script
DELETE FROM `instance_template` WHERE `map` = 2649;
INSERT INTO `instance_template` (`map`, `parent`, `script`) VALUES
(2649, 0, 'instance_asura_priory_of_the_void');

-- Spawns
DELETE FROM `creature` WHERE `guid` = @CGUID;
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnDifficulties`, `phaseUseFlags`, `PhaseId`, `PhaseGroup`, `terrainSwapMap`, `modelid`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curHealthPct`, `MovementType`, `npcflag`, `unit_flags`, `unit_flags2`, `unit_flags3`, `ScriptName`, `StringId`, `VerifiedBuild`) VALUES
(@CGUID, @BOSS, 2649, 0, 0, '1,2,8,23', 0, 0, 0, -1, 0, 0, 2936.5, 1824.4, 652.8, 4.71, 604800, 0, 0, 100, 0, NULL, NULL, NULL, NULL, '', NULL, 0);

DELETE FROM `gameobject` WHERE `guid` = @OGUID;
INSERT INTO `gameobject` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnDifficulties`, `phaseUseFlags`, `PhaseId`, `PhaseGroup`, `terrainSwapMap`, `position_x`, `position_y`, `position_z`, `orientation`, `rotation0`, `rotation1`, `rotation2`, `rotation3`, `spawntimesecs`, `animprogress`, `state`, `ScriptName`, `StringId`, `VerifiedBuild`) VALUES
-- on the Asura Sanctum island (map 9000), in front of the arrival point
(@OGUID, @PORTAL, 9000, 0, 0, '0', 0, 0, 0, -1, 1052.0, 1066.7, 50.84, 0, 0, 0, 0, 1, 120, 255, 1, '', NULL, 0);

-- GM teleport points
DELETE FROM `game_tele` WHERE `name` IN ('AsuraSanctum', 'AsuraPriory', 'AsuraNalazur');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES
((SELECT m FROM (SELECT MAX(id)+1 m FROM game_tele) t), 1066.7, 1066.7, 51.2, 3.14, 9000, 'AsuraSanctum');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES
((SELECT m FROM (SELECT MAX(id)+1 m FROM game_tele) t), 3021.4, 994.7, 514.3, 1.68, 2649, 'AsuraPriory');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES
((SELECT m FROM (SELECT MAX(id)+1 m FROM game_tele) t), 2936.5, 1840.0, 652.8, 4.71, 2649, 'AsuraNalazur');
