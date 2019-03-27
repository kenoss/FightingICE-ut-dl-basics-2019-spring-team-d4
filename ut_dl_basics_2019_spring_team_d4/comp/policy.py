__all__ = [
    'PolicyBase',
    'StatefulPolicyBase',
    'PolicyChain',
    'PolicyWaitRemainingFrame',
    'PolicyCycle',
    'PolicySingleAction',
    'PolicyWithEnoughtEnergy',
    'PolicyRandomWithFrames',
    'StatefulPolicyFrame',
    'StatefulPolicyFrameSingleAction',
    'PolicyRandomStatefulPolicies',
    'PolicyRandomStatefulPoliciesWithRetry',
    'PolicyWeightedRandomStatefulPoliciesWithRetry',
    'PolicyWithCompareDistanceX',
    'PolicyWithLessDistanceX',
    'PolicyWithMoreDistanceX',
    'PolicyWhenEnemyProjectileExist',
]


import numpy as np
import random

from .frame import FrameManager

from fice_nike.action import Action


def unzip(xss):
    return [list(xs) for xs in zip(*xss)]


class PolicyBase:
    def update(self, data):
        raise NotImplementedError()


class StatefulPolicyBase(PolicyBase):
    def new(self):
        raise NotImplementedError()

    def is_end(self):
        raise NotImplementedError()


class PolicyChain(PolicyBase):
    def __init__(self, policy_list):
        self._ps = policy_list

    def update(self, data):
        for p in self._ps:
            res = p.update(data)
            if res is not None:
                return res


class PolicyWaitRemainingFrame(PolicyBase):
    def __init__(self, threshold):
        assert threshold >= 0

        self._threshold = threshold

    def update(self, data):
        if data['frame_data'].getCharacter(data['player']).getRemainingFrame() > self._threshold:
            return Action.NEUTRAL


class PolicyCycle(PolicyBase):
    def __init__(self, policy_list):
        self._ps = policy_list
        self._i = -1

    def update(self, data):
        self._i = (self._i + 1) % len(self._ps)
        return self._ps[self._i].update(data)


class PolicySingleAction(PolicyBase):
    def __init__(self, action):
        self._action = action

    def update(self, _data):
        return self._action


class PolicyWithEnoughtEnergy(PolicyBase):
    def __init__(self, policy, threshold, transition_in_rate=1.0, transition_out_rate=1.0):
        self._policy = policy
        self._threshold = threshold
        self._in_rate = transition_in_rate
        self._out_rate = transition_out_rate
        self._flag = False

    def update(self, data):
        if data['frame_data'].getCharacter(data['player']).getEnergy() > self._threshold:
            if random.uniform(0, 1) <= self._in_rate:
                self._flag = True
        else:
            self._flag = False

        if self._flag:
            if random.uniform(0, 1) <= self._out_rate:
                self._flag = False
            return self._policy.update(data)


class PolicyRandomWithFrames(PolicyBase):
    def __init__(self, frame_manager_generator, policy_list):
        self._fm_gen = frame_manager_generator
        self._ps = policy_list
        self._curr_fm = FrameManager(0)
        self._curr_p = None

    def update(self, data):
        if self._curr_fm.is_end(data):
            self._curr_fm = self._fm_gen.generate()
            self._curr_p = random.choice(self._ps)

        return self._curr_p.update(data)


class StatefulPolicyFrame(StatefulPolicyBase):
    def __init__(self, frame, policy):
        self._frame = frame
        self._fm = None
        self._policy = policy
        self._is_end = False

    def new(self):
        return type(self)(self._frame, self._policy)

    def is_end(self):
        return self._is_end

    def update(self, data):
        if self._fm is None:
            self._fm = FrameManager(self._frame, data)

        if self._fm.is_end(data):
            self._is_end = True

        return self._policy.update(data)


class StatefulPolicyFrameSingleAction(StatefulPolicyFrame):
    def __init__(self, frame, action):
        super().__init__(frame, PolicySingleAction(action))

        self._frame = frame
        self._action = action

    def new(self):
        return type(self)(self._frame, self._action)


class PolicyRandomStatefulPolicies(StatefulPolicyBase):
    def __init__(self, stateful_policy_list):
        self._ps = stateful_policy_list
        self._p = self._new()

    def _new(self):
        return random.choice(self._ps).new()

    def update(self, data):
        res = self._p.update(data)

        if self._p.is_end():
            self._p = self._new()

        return res


class PolicyRandomStatefulPoliciesWithRetry(StatefulPolicyBase):
    def __init__(self, stateful_policy_list, retry=100):
        self._ps = stateful_policy_list
        self._p = self._new()
        self._retry = retry

    def _new(self):
        return random.choice(self._ps).new()

    def update(self, data):
        for _ in range(self._retry):
            res = self._p.update(data)

            if self._p.is_end():
                self._p = self._new()

            if res is not None:
                break

        return res


class PolicyWeightedRandomStatefulPoliciesWithRetry(StatefulPolicyBase):
    def __init__(self, weighted_stateful_policy_list, retry=100):
        ws, ps = unzip(weighted_stateful_policy_list)
        ws = np.array(ws)
        self._ws = ws / ws.sum()
        self._ps = ps
        self._is = np.arange(len(ps))
        self._p = self._new()
        self._retry = retry

    def _new(self):
        i = np.random.choice(self._is, p=self._ws)
        return self._ps[i].new()

    def update(self, data):
        for _ in range(self._retry):
            res = self._p.update(data)

            if self._p.is_end():
                self._p = self._new()

            if res is not None:
                break

        return res


# Absolute class
class PolicyWithCompareDistanceX(PolicyBase):
    COMPARE = None

    def __init__(self, distance, policy):
        self._d = distance
        self._p = policy

    def update(self, data):
        distance = data['frame_data'].getDistanceX()

        if self.COMPARE(distance, self._d):
            return self._p.update(data)
        else:
            return


class PolicyWithLessDistanceX(PolicyWithCompareDistanceX):
    COMPARE = lambda self, x, y: x < y


class PolicyWithMoreDistanceX(PolicyWithCompareDistanceX):
    COMPARE = lambda self, x, y: x > y


def exist_enemy_projectile(data):
    if data['player']:
        projectiles = data['frame_data'].getProjectilesByP2()
    else:
        projectiles = data['frame_data'].getProjectilesByP1()

    return len(projectiles) > 0


class PolicyWhenEnemyProjectileExist(PolicyBase):
    def __init__(self, policy):
        self._p = policy

    def update(self, data):
        if exist_enemy_projectile(data):
            return self._p.update(data)
        else:
            return
