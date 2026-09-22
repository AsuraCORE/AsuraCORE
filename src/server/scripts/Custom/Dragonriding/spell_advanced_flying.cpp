/*
 * This file is part of the TrinityCore Project. See AUTHORS file for Copyright information
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program. If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * AsuraCORE: ported from TheGhostGroup/DragonCore
 * (src/server/scripts/Spells/spell_advanced_flying.cpp), a GPL-2.0 TrinityCore
 * fork for client 10.2.x. Adapted here to our master's (client 12.1.0.69875)
 * movement/DB2/spell-script APIs. See src/server/scripts/Custom/Dragonriding
 * for the AsuraCORE-specific changes.
 *
 * Notable adaptations vs. the donor file:
 *  - GetAdvFlyingVelocity() no longer exists on Unit; our master tracks
 *    dragonriding velocity in the (client-reported) MovementInfo::advFlying
 *    struct, so we read caster->m_movementInfo.advFlying->forwardVelocity
 *    directly (m_movementInfo is a public member of WorldObject here).
 *  - Unit::AddMoveImpulse() does not exist on our master; there is no
 *    server-authoritative "add velocity" API for adv-flying movement yet.
 *    As a stand-in we use the existing Unit::KnockbackFrom() movement-force
 *    packet (same one used by knockback spells) to give the caster a
 *    forward/vertical push in the direction they are facing. This is an
 *    approximation of the client-side dragonriding impulse system and will
 *    need revisiting once/if native server-side adv-flying impulses are
 *    added to the core.
 *
 * Scripts for spells used by dragonriding and advanced fly spells.
 * Scriptnames of files in this file should be prefixed with "spell_af_".
 */

#include "DB2Stores.h"
#include "Player.h"
#include "ScriptMgr.h"
#include "Spell.h"
#include "SpellAuraEffects.h"
#include "SpellMgr.h"
#include "SpellScript.h"
#include <cmath>

enum AdvancedFlyingSpells
{
    SPELL_DRAGONRIDER_ENERGIZE      = 372606,
    SPELL_VIGOR_CACHE               = 433547,
    SPELL_RIDING_ABROAD             = 432503, // TODO outside of dragon isles
    SPELL_ENERGY_WIDGET             = 423624
};

// 373646 - Soar (Racial)
// 406095 - Skyriding
// 430833 - Soar (Racial)
class spell_af_skyriding : public AuraScript
{
    void OnApply(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
    {
        GetTarget()->CastSpell(GetTarget(), SPELL_ENERGY_WIDGET, true);
        GetTarget()->SetPower(POWER_ALTERNATE_MOUNT, GetTarget()->GetPower(POWER_ALTERNATE_MOUNT), true);
    }

    void OnRemove(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
    {
        GetTarget()->RemoveAurasDueToSpell(SPELL_ENERGY_WIDGET);
    }

    void Register() override
    {
        OnEffectApply += AuraEffectApplyFn(spell_af_skyriding::OnApply, EFFECT_2, SPELL_AURA_ANY, AURA_EFFECT_HANDLE_REAL);
        OnEffectRemove += AuraEffectRemoveFn(spell_af_skyriding::OnRemove, EFFECT_2, SPELL_AURA_ANY, AURA_EFFECT_HANDLE_REAL);
    }
};

// 372773 - Dragonrider Energy
class spell_af_energy : public AuraScript
{
    void OnApply(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
    {
        Unit* target = GetTarget();
        if (!target->HasAura(SPELL_VIGOR_CACHE))
        {
            CastSpellExtraArgs extraArgs(TRIGGERED_FULL_MASK);
            extraArgs.AddSpellMod(SPELLVALUE_BASE_POINT0, target->GetPower(POWER_ALTERNATE_MOUNT));
            target->CastSpell(target, SPELL_VIGOR_CACHE, extraArgs);
        }
    }

    void OnPeriodic(AuraEffect* /*aurEff*/)
    {
        if (Unit* caster = GetCaster())
        {
            if (ShouldRegenEnergy(caster))
            {
                if (AuraEffect* subAmountAurEff = caster->GetAuraEffect(SPELL_VIGOR_CACHE, EFFECT_1))
                {
                    int32 baseRegen = 20; // Todo : Calculate this based on talents & if we are thrilled/grounded

                    int32 newAmount = subAmountAurEff->GetAmount() + baseRegen;

                    if (newAmount >= 100)
                    {
                        newAmount -= 100;

                        caster->CastSpell(caster, SPELL_DRAGONRIDER_ENERGIZE, TRIGGERED_FULL_MASK);

                        if (AuraEffect* amountAurEff = caster->GetAuraEffect(SPELL_VIGOR_CACHE, EFFECT_0))
                            amountAurEff->SetAmount(caster->GetPower(POWER_ALTERNATE_MOUNT));
                    }

                    subAmountAurEff->SetAmount(newAmount);
                    subAmountAurEff->GetBase()->SetNeedClientUpdateForTargets();
                }

                int newMaxPower = 3;

                if (caster->HasAura(377920) && !caster->HasAura(377921) && !caster->HasAura(377922))
                {
                    newMaxPower = 4;
                }
                else if (caster->HasAura(377921) && caster->HasAura(377920) && !caster->HasAura(377922))
                {
                    newMaxPower = 5;
                }
                else if (caster->HasAura(377922) && caster->HasAura(377921) && caster->HasAura(377920))
                {
                    newMaxPower = 6;
                }

                caster->SetMaxPower(POWER_ALTERNATE_MOUNT, newMaxPower);
            }
        }
    }

    void OnRemove(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
    {
        GetTarget()->RemoveAurasDueToSpell(SPELL_VIGOR_CACHE);
    }

    void Register() override
    {
        OnEffectApply += AuraEffectApplyFn(spell_af_energy::OnApply, EFFECT_0, SPELL_AURA_ENABLE_ALT_POWER, AURA_EFFECT_HANDLE_REAL);
        OnEffectUpdatePeriodic += AuraEffectUpdatePeriodicFn(spell_af_energy::OnPeriodic, EFFECT_1, SPELL_AURA_PERIODIC_DUMMY);
        OnEffectRemove += AuraEffectRemoveFn(spell_af_energy::OnRemove, EFFECT_0, SPELL_AURA_ENABLE_ALT_POWER, AURA_EFFECT_HANDLE_REAL);
    }

private:
    // AsuraCORE: donor used Unit::GetAdvFlyingVelocity(), which does not
    // exist on our master. Our master already stores the client-reported
    // adv-flying velocity in the public MovementInfo::advFlying member, so
    // read it from there instead.
    bool ShouldRegenEnergy(Unit const* caster) const
    {
        if (caster->GetPower(POWER_ALTERNATE_MOUNT) == caster->GetMaxPower(POWER_ALTERNATE_MOUNT))
            return false;

        FlightCapabilityEntry const* flightCapabilityEntry = sFlightCapabilityStore.LookupEntry(caster->GetFlightCapabilityID());
        if (!flightCapabilityEntry)
            return false;

        float velocity = caster->m_movementInfo.advFlying ? caster->m_movementInfo.advFlying->forwardVelocity : 0.0f;

        float velocityRegenThreshold = flightCapabilityEntry->MaxVel * flightCapabilityEntry->VigorRegenMaxVelCoefficient;
        if (velocity >= velocityRegenThreshold)
            return true;

        // AsuraCORE: donor used Unit::IsInAir(), which does not exist on our
        // master. Approximate it from the existing movement flags instead.
        bool inAir = caster->HasUnitMovementFlag(MovementFlags(MOVEMENTFLAG_FLYING | MOVEMENTFLAG_DISABLE_GRAVITY | MOVEMENTFLAG_FALLING | MOVEMENTFLAG_FALLING_FAR));
        return !inAir || caster->IsInWater();
    }
};

// AsuraCORE: donor's spell_af_skyward_ascent / spell_af_surge_forward /
// spell_af_whirling_surge all called a custom Unit::AddMoveImpulse() that
// does not exist on our master (no server-authoritative "add velocity" API
// for adv-flying exists in core yet). Re-implemented on top of the existing
// Unit::KnockbackFrom() movement-force packet instead: passing the caster's
// own position as the knockback origin with angle 0 pushes them in the
// direction they are currently facing, which approximates the donor's
// forward/vertical impulse. This is a stopgap until true adv-flying
// impulses are implemented in the core movement system.

// 374763 - Lift off
// 372610 - Skyward Ascent (Dragonriding)
class spell_af_skyward_ascent : public SpellScript
{
    void HandleHitTarget(SpellEffIndex effIndex)
    {
        if (Player* caster = GetCaster()->ToPlayer())
        {
            float ascentSpeed = float(uint32(GetSpellValue()->EffectBasePoints[effIndex])) / 10.0f;
            caster->KnockbackFrom(caster->GetPosition(), 0.0f, ascentSpeed, 0.0f);
        }
    }

    void Register() override
    {
        OnEffectHitTarget += SpellEffectFn(spell_af_skyward_ascent::HandleHitTarget, EFFECT_0, SPELL_EFFECT_DUMMY);
    }
};

// 372608 - Surge Forward
class spell_af_surge_forward : public SpellScript
{
    void HandleHitTarget(SpellEffIndex /*effIndex*/)
    {
        if (Player* caster = GetCaster()->ToPlayer())
        {
            float SURGE_SPEED = 14.0f;
            float speedZ = SURGE_SPEED * std::tan(caster->m_movementInfo.pitch);

            caster->KnockbackFrom(caster->GetPosition(), SURGE_SPEED, speedZ, 0.0f);
        }
    }

    void Register() override
    {
        OnEffectHitTarget += SpellEffectFn(spell_af_surge_forward::HandleHitTarget, EFFECT_0, SPELL_EFFECT_DUMMY);
    }
};

// 361584 - Whirling Surge
class spell_af_whirling_surge : public SpellScript
{
    void HandleHitTarget(SpellEffIndex /*effIndex*/)
    {
        if (Player* caster = GetCaster()->ToPlayer())
        {
            float SURGE_SPEED = 60.0f;
            float speedZ = SURGE_SPEED * std::tan(caster->m_movementInfo.pitch);

            caster->KnockbackFrom(caster->GetPosition(), SURGE_SPEED, speedZ, 0.0f);
        }
    }

    void Register() override
    {
        OnEffectHitTarget += SpellEffectFn(spell_af_whirling_surge::HandleHitTarget, EFFECT_0, SPELL_EFFECT_APPLY_AURA);
    }
};

void AddSC_advanced_flying_spell_scripts()
{
    RegisterSpellScript(spell_af_skyriding);
    RegisterSpellScript(spell_af_energy);
    RegisterSpellScript(spell_af_skyward_ascent);
    RegisterSpellScript(spell_af_surge_forward);
    RegisterSpellScript(spell_af_whirling_surge);
}
