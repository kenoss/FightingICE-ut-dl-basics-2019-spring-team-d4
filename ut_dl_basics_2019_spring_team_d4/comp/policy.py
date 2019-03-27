__all__ = [
    'PolicyBase',
    'PolicyChain',
    'PolicyWaitRemainingFrame',
    'PolicyCycle',
    'PolicySingleAction',
    'PolicyWithEnoughtEneregy'
]


import random


class PolicyBase:
    def update(self, data):
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
            return '_'


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


class PolicyWithEnoughtEneregy(PolicyBase):
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
