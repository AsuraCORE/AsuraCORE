# Свой контент: куда что класть

| Хочу | Где делается | Нужен ли клиентский файл |
|---|---|---|
| Свой NPC, лут, вендор, квест | БД `world` (`creature_template`, `quest_template`, …) | нет |
| Свой предмет или спелл | БД `hotfixes` (Item, ItemSparse, SpellName, SpellMisc, …): сервер сам шлёт клиенту hotfix | нет |
| Механики босса или подземелья | C++ в `core/src/server/scripts/Custom/` (BossAI, InstanceScript) | нет |
| Новая модель, текстура, звук | файл + Arctium `mappings/*.txt` | **да** |
| Новая локация или карта | ADT/WDT/WMO + записи в `Map`, `AreaTable` (hotfixes) + извлечение maps/vmaps/mmaps | **да** |

## Правила, чтобы не мучиться с мерджами upstream
- Весь свой C++ держи в `src/server/scripts/Custom/` и регистрируй в `custom_script_loader.cpp`.
- Свой SQL клади в `sql/custom/`. Для ID используй свой диапазон, например creature/item/spell от **900000**, чтобы не пересекаться с Blizzard.
- Если правишь ядро (`src/server/game`), помечай изменения комментарием `// AsuraCORE:`.

## Первые шаги
1. Свой предмет через hotfixes: скопировать существующий ItemSparse, поменять ID/имя/статы.
2. Свой NPC-босс с 2–3 фазами в `scripts/Custom/` (образцы: любые `boss_*.cpp` в `src/server/scripts/`).
3. Замена текстуры через Arctium, чтобы проверить весь путь custom files.
