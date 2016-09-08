import json
import re
from flexObject import FlexObject, isNumericAttr, isBoolean, boolFromString, isListAttr
class FlexActionObject(FlexObject) :


    def createExecuteActionMethod (self, fileHdl):
        tabs = self.TAB
        #lines = [ "\n"+ tabs + "@processReturnCode"]
        lines = []
        lines.append("\n"+ tabs + "def update" + self.name + "(self,")
        tabs = tabs + self.TAB
        spaces = ' ' * (len(lines[-1])  - len("self, "))
        objLines = [tabs + "obj =  {}\n"]
        for (attr, attrInfo) in self.attrList:
            if attrInfo['isKey'] != 'True':
                lines.append("\n" + spaces + "%s = None," %(attr))
            else:
                lines.append("\n" + spaces + "%s," %(attr))
            objLines.append(tabs + "if %s != None :\n" %(attr))
            assignmentStr =''
            if isNumericAttr(attrInfo):
                assignmentStr = "int(%s)" %(attr)
            elif isBoolean(attrInfo['type']):
                assignmentStr = "True if %s else False" %(attr)
            else:
                assignmentStr = "%s" %(attr)
            objLines.append(tabs + self.TAB + "obj[\'%s\'] = %s\n\n" %(attr, assignmentStr))
        lines[-1] = lines[-1][0:lines[-1].find(',')]
        lines.append("):\n")
        lines = lines + objLines
        lines.append (tabs + "reqUrl =  self.cfgUrlBase+" +"\'%s\'\n" %(self.name))
        lines.append(tabs + "r = requests.patch(reqUrl, data=json.dumps(obj), headers=headers) \n")
        lines.append(tabs + "return r\n")
        fileHdl.writelines(lines)



    def writeAllMethods (self, fileHdl):
        self.createExecuteActionMethod(fileHdl)

