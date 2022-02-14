
class Rule:
    def __init__(self, attributes, decision):
        self.attributes = attributes
        self.decision = decision

    def __str__(self):
        string_rule = ''
        for (attribute, value) in self.attributes.items():
            string_rule += '{}={} '.format(attribute, value)
        string_rule += 'd={}'.format(self.decision)
        return string_rule