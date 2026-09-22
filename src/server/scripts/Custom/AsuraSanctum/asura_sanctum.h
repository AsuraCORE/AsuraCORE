/*
 * AsuraCORE custom content: Void Sanctum hub (Voidstorm) and the Priory of the Void instance.
 */

#ifndef ASURA_SANCTUM_H_
#define ASURA_SANCTUM_H_

#include "CreatureAIImpl.h"
#include "Position.h"

constexpr char const* AsuraSanctumScriptName = "instance_asura_priory_of_the_void";
constexpr char const* AsuraSanctumDataHeader = "APV";

// Priory of the Sacred Flame map, reused as our instance
constexpr uint32 MAP_ASURA_PRIORY = 2649;
// Voidstorm (Midnight zone), our hub
constexpr uint32 MAP_ASURA_HUB    = 2771;

constexpr uint32 EncounterCount = 1;

enum AsuraSanctumData
{
    DATA_NALAZUR = 0
};

enum AsuraSanctumCreatures
{
    NPC_NALAZUR    = 900000,
    NPC_VOID_SPAWN = 900001
};

enum AsuraSanctumGameObjects
{
    GO_VOID_PORTAL = 900000
};

Position const AsuraHubPortalExit     = { 1915.0f,  595.5f, -180.0f, 4.73f }; // where players land in the hub
Position const AsuraInstanceEntrance  = { 3021.4f,  994.7f,  514.3f, 1.68f }; // instance entrance
Position const AsuraExitPortalSpawn   = { 2936.5f, 1834.4f,  652.8f, 4.71f }; // exit portal after the boss dies

template <class AI, class T>
inline AI* GetAsuraSanctumAI(T* obj)
{
    return GetInstanceAI<AI>(obj, AsuraSanctumScriptName);
}

#define RegisterAsuraSanctumCreatureAI(ai_name) RegisterCreatureAIWithFactory(ai_name, GetAsuraSanctumAI)

#endif // ASURA_SANCTUM_H_
