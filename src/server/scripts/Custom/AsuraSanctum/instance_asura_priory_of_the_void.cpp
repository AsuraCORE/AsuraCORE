/*
 * AsuraCORE custom content: instance script for the Priory of the Void.
 */

#include "InstanceScript.h"
#include "ScriptMgr.h"
#include "asura_sanctum.h"

static constexpr ObjectData creatureData[] =
{
    { NPC_NALAZUR, DATA_NALAZUR }
};

class instance_asura_priory_of_the_void : public InstanceMapScript
{
public:
    instance_asura_priory_of_the_void() : InstanceMapScript(AsuraSanctumScriptName, MAP_ASURA_PRIORY) { }

    struct instance_asura_priory_of_the_void_InstanceMapScript : public InstanceScript
    {
        instance_asura_priory_of_the_void_InstanceMapScript(InstanceMap* map) : InstanceScript(map)
        {
            SetHeaders(AsuraSanctumDataHeader);
            SetBossNumber(EncounterCount);
            LoadObjectData(creatureData, {});
        }
    };

    InstanceScript* GetInstanceScript(InstanceMap* map) const override
    {
        return new instance_asura_priory_of_the_void_InstanceMapScript(map);
    }
};

void AddSC_instance_asura_priory_of_the_void()
{
    new instance_asura_priory_of_the_void();
}
