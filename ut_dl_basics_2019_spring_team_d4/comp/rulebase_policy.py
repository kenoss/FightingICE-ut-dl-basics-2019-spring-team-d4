__all__ = [
    'RulebasePolicyBase',
    'RulebasePolicyRandomAlpha',
    'RulebasePolicyWrfWeepRandomAlpha',
    'RulebasePolicyWrfWeepNoAction',
    'RulebasePolicyWepegWeepRandomAlpha',
    'RulebasePolicyGarnet',
]



from .policy import *

from fice_nike.action import Action


class RulebasePolicyBase(PolicyBase):
    _inner = None

    def update(self, data):
        return self._inner.update(data)


class RulebasePolicyRandomAlpha(RulebasePolicyBase):
    def __init__(self):
        self._inner = PolicyWeightedRandomStatefulPoliciesWithRetry([
            # Move
            ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(50, PolicySingleAction(Action.MOVE_F)))),
            ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(100, PolicySingleAction(Action.MOVE_FF)))),
            ( 10, StatefulPolicyFrame(1, PolicySingleAction(Action.MOVE_BB))),

            # Moving attack
            ( 30, StatefulPolicyFrame(30, PolicyCycle([PolicySingleAction(Action.MOVE_F), PolicySingleAction(Action.A)]))),
            ( 30, StatefulPolicyFrame(30, PolicyCycle([PolicySingleAction(Action.MOVE_F), PolicySingleAction(Action.B)]))),

            # Simple attack
            ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicySingleAction(Action.A)))),
            ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicySingleAction(Action.B)))),
            ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicySingleAction(Action.STAND_FA)))),
            ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicyWithMoreDistanceX(150, PolicySingleAction(Action.STAND_FB))))),

            # Crouch
            # # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(20, PolicySingleAction(Action.MOVE_D)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(50, PolicySingleAction(Action.CROUCH_A)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(50, PolicySingleAction(Action.CROUCH_B)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(50, PolicySingleAction(Action.CROUCH_FA)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(50, PolicySingleAction(Action.CROUCH_FB)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(200, PolicySingleAction(Action.STAND_D_DF_FA)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(200, PolicySingleAction(Action.STAND_D_DF_FB)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(100, PolicySingleAction(Action.STAND_F_D_DFA)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(200, PolicySingleAction(Action.STAND_F_D_DFB)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicySingleAction(Action.STAND_D_DB_BA)))),
            # ( 30, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicySingleAction(Action.STAND_D_DB_BB)))),

            # Jump attack
            # ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_U), PolicySingleAction(Action.AIR_DA)]))),
            # ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_U), PolicySingleAction(Action.AIR_DB)]))),
            # ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_U), PolicySingleAction(Action.AIR_FA)]))),
            # ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_U), PolicySingleAction(Action.AIR_FB)]))),
            # ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_U), PolicySingleAction(Action.AIR_UA)]))),
            # ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_U), PolicySingleAction(Action.AIR_UB)]))),
            ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_UF), PolicySingleAction(Action.AIR_DA)]))),
            ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_UF), PolicySingleAction(Action.AIR_DB)]))),
            ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_UF), PolicySingleAction(Action.AIR_FA)]))),
            ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_UF), PolicySingleAction(Action.AIR_FB)]))),
            ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_UF), PolicySingleAction(Action.AIR_UA)]))),
            ( 10, StatefulPolicyFrame(10, PolicyCycle([PolicySingleAction(Action.MOVE_UF), PolicySingleAction(Action.AIR_UB)]))),
        ])


class RulebasePolicyWrfWeepRandomAlpha(RulebasePolicyBase):
    ENERGY_THRESHOLD = 20
    PROB_IN = 0.99999
    PROB_OUT = 1.0

    def __init__(self):
        self._inner = PolicyChain([
            PolicyWaitRemainingFrame(10),
            # PolicyWithEnoughtEnergy(PolicySingleAction(Action.PROJECTILE), 10, 0.9, 1.0),
            PolicyWithEnoughtEnergy(
                PolicyWeightedRandomStatefulPoliciesWithRetry([
                    ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.NEUTRAL)))),
                    ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.PROJECTILE)))),
                    ( 10, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicySingleAction(Action.MOVE_BB)))),
                ]),
                self.ENERGY_THRESHOLD, self.PROB_IN, self.PROB_OUT,
            ),
            RulebasePolicyRandomAlpha(),
        ])


class RulebasePolicyWrfWeepNoAction(RulebasePolicyBase):
    ENERGY_THRESHOLD = 20
    PROB_IN = 1.0
    PROB_OUT = 0.0

    def __init__(self):
        self._inner = PolicyChain([
            PolicyWaitRemainingFrame(10),
            # PolicyWithEnoughtEnergy(PolicySingleAction(Action.PROJECTILE), 10, 0.9, 1.0),
            PolicyWithEnoughtEnergy(
                PolicyWeightedRandomStatefulPoliciesWithRetry([
                    ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.NEUTRAL)))),
                    ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.PROJECTILE)))),
                    ( 10, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicySingleAction(Action.MOVE_BB)))),
                ]),
                self.ENERGY_THRESHOLD, self.PROB_IN, self.PROB_OUT,
            ),
        ])


class RulebasePolicyWepegWeepRandomAlpha(RulebasePolicyBase):
    ENERGY_THRESHOLD = 100
    PROB_IN = 0.99999
    PROB_OUT = 1.0

    def __init__(self):
        self._inner = PolicyChain([
            PolicyWhenEnemyProjectileExist(PolicySingleAction(Action.MOVE_UF)),
            PolicyWithEnoughtEnergy(
                PolicyWeightedRandomStatefulPoliciesWithRetry([
                    ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.NEUTRAL)))),
                    ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.PROJECTILE)))),
                    ( 10, StatefulPolicyFrame(1, PolicyWithLessDistanceX(300, PolicySingleAction(Action.MOVE_BB)))),
                ]),
                self.ENERGY_THRESHOLD, self.PROB_IN, self.PROB_OUT,
            ),
            RulebasePolicyRandomAlpha(),
        ])


class RulebasePolicyGarnet(RulebasePolicyBase):
    ENERGY_THRESHOLD = 40
    PROB_IN = 0.99999
    PROB_OUT = 1.0

    def __init__(self):
        self._inner = PolicyChain([
            PolicyWhenEnemyProjectileExist(PolicySingleAction(Action.MOVE_UF)),
            PolicyWithEnoughtEnergy(
                # 近づいて飛び膝蹴りを食らわす戦法が Garnet 的には強かった.
                PolicyWeightedRandomStatefulPoliciesWithRetry([
                    # ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.PROJECTILE)))),
                    # ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.STAND_D_DF_FA)))), # 消費 20 小さい波動拳
                    ( 10, StatefulPolicyFrame(1, PolicyWithLessDistanceX(50, PolicySingleAction(Action.STAND_F_D_DFB)))), # 消費 45 飛び膝蹴り
                    # ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(300, PolicySingleAction(Action.STAND_D_DB_BB)))), # 消費 30 足払い
                    ( 10, StatefulPolicyFrame(1, PolicyWithMoreDistanceX(50, PolicySingleAction(Action.MOVE_F)))),
                ]),
                self.ENERGY_THRESHOLD, self.PROB_IN, self.PROB_OUT,
            ),
            RulebasePolicyRandomAlpha(),
        ])
