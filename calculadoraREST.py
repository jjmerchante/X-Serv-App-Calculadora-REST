import webapp
import re


class calcRest(webapp.webApp):

    def __init__(self, hostname, port):
        self.oper = None
        webapp.webApp.__init__(self, hostname, port)

    def getResult(self, operation):
        try:
            (strNum1, strNum2) = re.split('\+|\-|\*|\/', operation)
            num1 = float(strNum1)
            num2 = float(strNum2)
        except ValueError:
            return None
        if len(operation.split('+')) == 2:
            return str(num1 + num2)
        elif len(operation.split('-')) == 2:
            return str(num1 - num2)
        elif len(operation.split('*')) == 2:
            return str(num1 * num2)
        elif len(operation.split('/')) == 2:
            if num2 == 0:
                return "NaN"
            return str(num1 / num2)
        else:
            return None

    def parse(self, request):
        head = request.split("\r\n\r\n")[0]
        body = request.split("\r\n\r\n")[1]
        httpVerb = head.split(" ")[0]
        return (httpVerb, body)

    def process(self, (httpVerb, body)):
        if httpVerb == "PUT":
            self.oper = body
            code = "200 OK"
            answer = "Operacion: " + body

        elif httpVerb == "GET":
            if self.oper is None:
                code = "400 Not found"
                answer = "You must PUT first"
            else:
                result = self.getResult(self.oper)
                if result is None:
                    code = "400 Not found"
                    answer = self.oper + ": No result"
                else:
                    code = "200 OK"
                    answer = self.oper + " = " + result

        else:
            code = "400 Not Found"
            answer = "Invalid operation"
        return (code, "<html><body><h1>" + answer +
                "</h1></body></html>")


if __name__ == '__main__':
    testWebApp = calcRest("localhost", 1235)
