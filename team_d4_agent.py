__all__ = [
    'TeamD4Agent',
]


from ut_dl_basics_2019_spring_team_d4.comp.rulebase_agent import *


class TeamD4Agent(RulebaseAgentGarnet):
    def getCharacter(self):
        return 'GARNET'
