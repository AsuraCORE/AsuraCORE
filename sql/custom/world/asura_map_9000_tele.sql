-- AsuraCORE: GM teleport to the new map 9000 (Asura Sanctum island)
DELETE FROM `game_tele` WHERE `name` = 'AsuraIsland';
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`)
SELECT MAX(`id`) + 1, 1066.67, 1066.67, 62, 0, 9000, 'AsuraIsland' FROM `game_tele`;
