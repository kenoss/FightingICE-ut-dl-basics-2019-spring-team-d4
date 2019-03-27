__all__ = [
    'RulebaseAgentBase',
    'RulebaseAgentRandomAlpha',
    'RulebaseAgentWrfWeepRandomAlpha',
    'RulebaseAgentWrfWeepNoAction',
    'RulebaseAgentWepegWeepRandomAlpha',
    'RulebaseAgentGarnet',
]


from .rulebase_policy import *

from fice_nike.agent_base import AgentBase


class RulebaseAgentBase(AgentBase):
    _policy = None

    def __init__(self, *args):
        super().__init__(*args)

    def policy(self, frame_data):
        data = {
            'frame_data': frame_data,
            'player':     self.player,
        }
        return self._policy.update(data)


class RulebaseAgentRandomAlpha(RulebaseAgentBase):
    def __init__(self, *args):
        super().__init__(*args)

        self._policy = RulebasePolicyRandomAlpha()


class RulebaseAgentWrfWeepRandomAlpha(RulebaseAgentBase):
    def __init__(self, *args):
        super().__init__(*args)

        self._policy = RulebasePolicyWrfWeepRandomAlpha()


class RulebaseAgentWrfWeepNoAction(RulebaseAgentBase):
    def __init__(self, *args):
        super().__init__(*args)

        self._policy = RulebasePolicyWrfWeepNoAction()


class RulebaseAgentWepegWeepRandomAlpha(RulebaseAgentBase):
    def __init__(self, *args):
        super().__init__(*args)

        self._policy = RulebasePolicyWepegWeepRandomAlpha()

class RulebaseAgentGarnet(RulebaseAgentBase):
    def __init__(self, *args):
        super().__init__(*args)

        self._policy = RulebasePolicyGarnet()
