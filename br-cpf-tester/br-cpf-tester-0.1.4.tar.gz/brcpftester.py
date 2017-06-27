import sys
from re import match


class BrazilianCpfValidationTests:
    """
    Class to test the Brazilian CPF number
    
    """

    MESSAGES = {
        'charformat': 'CPF deve ter o formato XXX.XXX.XXX-XX.',
        'digits': 'CPF deve conter apenas números.',
        'length': 'CPF deve conter 11 números.',
        'checkdigits': 'CPF inválido.',
    }


    def __init__(self, considered_tests=None):

        if considered_tests:
            self.considered_tests = considered_tests
        else:
            self.considered_tests = self.MESSAGES.keys()


    def __call__(self, value):

        self.tests = []
        self.cpf = value
        self.Tests()


    def _clean_cpf(self, value):

        return ''.join([x for x in value if x not in '.-'])


    def _append_test(self, code):

        if code in self.considered_tests:
            self.tests.append(code)


    def _calcule_cpfdigit_aux(self, value):

        total = 0
        weight = 9

        for x in reversed(value):
            total += int(x) * weight
            weight += -1

        cpfdigit = total % 11

        if cpfdigit == 10:
            cpfdigit = 0

        return str(cpfdigit)


    def CalculateDigit(self, value):

        number_of_digits = 2

        for i in range(0, number_of_digits):
            value = value + self._calcule_cpfdigit_aux(value)

        return value[-number_of_digits:]


    def Tests(self):

        self.cpf_original = self.cpf
        self.cpfdigit_original = self.cpf[-2:]
        self.cpf_cleaned = self._clean_cpf(self.cpf)
        self.cpf_firstpart = self.cpf_cleaned[:-2]

        if len(self.cpf) != len(self.cpf_cleaned) and not match('\d{3}\.\d{3}\.\d{3}\-\d{2}', self.cpf):
            self._append_test('charformat')

        if not self.cpf_cleaned.isdigit():
            self._append_test('digits')
            self.cpfdigit_calculated = ''
        else:
            self.cpfdigit_calculated = self.CalculateDigit(self.cpf_firstpart)

        if len(self.cpf_cleaned) != 11:
            self._append_test('length')

        if not self.cpfdigit_original == self.cpfdigit_calculated:
            self._append_test('checkdigits')


    def GetMessage(self, testcode):

        if not testcode in self.MESSAGES:
            return testcode

        return self.MESSAGES[testcode]


def main():
    args = sys.argv[1:]

    ignorecheckdigits = False
    if len(args)>0 and args[0] == '--ignorecheckdigits':
        ignorecheckdigits = True
        del args[0]

    onlydigits = False
    if len(args)>0 and args[0] == '--onlydigits':
        onlydigits = True
        del args[0]

    if not args:
        print('usage: [--ignorecheckdigits] [--onlydigits] cpfnumber [cpfnumber ...]')
        sys.exit(1)

    considered_tests = ['digits','length',]
    if not ignorecheckdigits:
        considered_tests.append('checkdigits')

    if not onlydigits:
        considered_tests.append('charformat')

    cpf = BrazilianCpfValidationTests(considered_tests)

    for cpfvalue in args:
        # For each cpfnumber, get the validity test
        cpf(cpfvalue)
        if not cpf.tests:
            check = 'OK'
        else:
            check = 'KO ( '
            for code in cpf.tests:
                check += cpf.GetMessage(code)+"  "
            check +=')'
        print("{:>14} : {}".format(cpf.cpf_original,check))

if __name__ == '__main__':
    main()
