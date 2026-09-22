/*
 * AsuraCORE custom content: Nal'Azur, Warden of the Void - final boss of the Priory of the Void,
 * his Void Spawn adds and the Void Portal that links the Voidstorm hub with the instance.
 *
 * Phase 1 (100-60%): Shadow Bolt on the tank, Shadow Bolt Volley.
 * Phase 2 (60-30%):  summons Void Spawns, Shadow Nova knockback.
 * Phase 3 (<30%):    enrages, faster volleys.
 */

#include "GameObject.h"
#include "GameObjectAI.h"
#include "InstanceScript.h"
#include "Map.h"
#include "ObjectAccessor.h"
#include "Player.h"
#include "ScriptMgr.h"
#include "ScriptedCreature.h"
#include "asura_sanctum.h"

enum NalazurSpells
{
    SPELL_SHADOW_BOLT        = 30055,
    SPELL_SHADOW_BOLT_VOLLEY = 15245,
    SPELL_SHADOW_NOVA        = 30852,
    SPELL_ENRAGE             = 8599
};

enum NalazurEvents
{
    EVENT_SHADOW_BOLT = 1,
    EVENT_VOLLEY,
    EVENT_SUMMON_SPAWNS,
    EVENT_SHADOW_NOVA
};

enum NalazurPhases
{
    PHASE_ONE   = 1,
    PHASE_TWO   = 2,
    PHASE_THREE = 3
};

struct boss_nalazur : public BossAI
{
    boss_nalazur(Creature* creature) : BossAI(creature, DATA_NALAZUR), _phase(PHASE_ONE) { }

    void Reset() override
    {
        _Reset();
        _phase = PHASE_ONE;
    }

    void JustEngagedWith(Unit* who) override
    {
        BossAI::JustEngagedWith(who);
        me->Yell("Свет здесь угас давно. Вы станете частью Пустоты!", LANG_UNIVERSAL);

        events.ScheduleEvent(EVENT_SHADOW_BOLT, 3s);
        events.ScheduleEvent(EVENT_VOLLEY, 12s);
    }

    void DamageTaken(Unit* /*attacker*/, uint32& damage, DamageEffectType /*damageType*/, SpellInfo const* /*spellInfo*/) override
    {
        if (_phase == PHASE_ONE && me->HealthBelowPctDamaged(60, damage))
        {
            _phase = PHASE_TWO;
            me->Yell("Порождения Пустоты, ко мне!", LANG_UNIVERSAL);
            events.ScheduleEvent(EVENT_SUMMON_SPAWNS, 1s);
            events.ScheduleEvent(EVENT_SHADOW_NOVA, 8s);
        }
        else if (_phase == PHASE_TWO && me->HealthBelowPctDamaged(30, damage))
        {
            _phase = PHASE_THREE;
            me->Yell("Довольно! Пустота поглотит всё!", LANG_UNIVERSAL);
            DoCastSelf(SPELL_ENRAGE, true);
            events.RescheduleEvent(EVENT_VOLLEY, 3s);
        }
    }

    void JustSummoned(Creature* summon) override
    {
        BossAI::JustSummoned(summon);
        DoZoneInCombat(summon);
    }

    void KilledUnit(Unit* victim) override
    {
        if (victim->IsPlayer())
            me->Yell("Ещё одна искра погасла.", LANG_UNIVERSAL);
    }

    void JustDied(Unit* /*killer*/) override
    {
        _JustDied();
        me->Yell("Пустота... не забудет... этого...", LANG_UNIVERSAL);
        me->SummonGameObject(GO_VOID_PORTAL, AsuraExitPortalSpawn, QuaternionData::fromEulerAnglesZYX(AsuraExitPortalSpawn.GetOrientation(), 0.0f, 0.0f), 30min);
    }

    void UpdateAI(uint32 diff) override
    {
        if (!UpdateVictim())
            return;

        events.Update(diff);

        if (me->HasUnitState(UNIT_STATE_CASTING))
            return;

        while (uint32 eventId = events.ExecuteEvent())
        {
            switch (eventId)
            {
                case EVENT_SHADOW_BOLT:
                    DoCastVictim(SPELL_SHADOW_BOLT);
                    events.Repeat(4s, 6s);
                    break;
                case EVENT_VOLLEY:
                    DoCastSelf(SPELL_SHADOW_BOLT_VOLLEY);
                    events.Repeat(_phase == PHASE_THREE ? 8s : 15s);
                    break;
                case EVENT_SUMMON_SPAWNS:
                    for (uint8 i = 0; i < 2; ++i)
                        me->SummonCreature(NPC_VOID_SPAWN, me->GetRandomNearPosition(10.0f), TEMPSUMMON_CORPSE_TIMED_DESPAWN, 10s);
                    events.Repeat(25s);
                    break;
                case EVENT_SHADOW_NOVA:
                    DoCastSelf(SPELL_SHADOW_NOVA);
                    events.Repeat(20s);
                    break;
                default:
                    break;
            }

            if (me->HasUnitState(UNIT_STATE_CASTING))
                return;
        }
    }

private:
    uint8 _phase;
};

// Two-way portal: Voidstorm hub -> Priory of the Void entrance, and back from inside the instance.
struct go_asura_void_portal : public GameObjectAI
{
    go_asura_void_portal(GameObject* go) : GameObjectAI(go) { }

    bool OnGossipHello(Player* player) override
    {
        if (player->IsInCombat())
            return true;

        if (me->GetMapId() == MAP_ASURA_PRIORY)
            player->TeleportTo(MAP_ASURA_HUB, AsuraHubPortalExit.GetPositionX(), AsuraHubPortalExit.GetPositionY(), AsuraHubPortalExit.GetPositionZ(), AsuraHubPortalExit.GetOrientation());
        else
            player->TeleportTo(MAP_ASURA_PRIORY, AsuraInstanceEntrance.GetPositionX(), AsuraInstanceEntrance.GetPositionY(), AsuraInstanceEntrance.GetPositionZ(), AsuraInstanceEntrance.GetOrientation());

        return true;
    }
};

void AddSC_boss_nalazur()
{
    RegisterAsuraSanctumCreatureAI(boss_nalazur);
    RegisterGameObjectAI(go_asura_void_portal);
}
