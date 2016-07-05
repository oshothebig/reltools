import json
import re
from flexObject import FlexObject, isNumericAttr, isBoolean, boolFromString, isListAttr
class FlexConfigObject(FlexObject) :

    def createCreateMethod(self, fileHdl):
        tabs = self.TAB
        #lines = [ "\n"+ tabs + "@processReturnCode"]
        lines = []
        lines.append( "\n"+ tabs + "def create" + self.name + "(self,")
        docLines = [ "\n" + tabs + "\"\"\"" +"\n" + tabs + ".. automethod :: create%s(self,\n" %(self.name)]
        #docLines.append("\n"+ tabs + "Parameters")
        #docLines.append("\n"+ tabs + "----------"+"\n")
        tabs = tabs + self.TAB
        spaces = ' ' * (len(lines[-1])  - len("self, "))
        objLines = [tabs + "obj =  { \n"]
        for (attr, attrInfo) in self.attrList:
            assignmentStr = ''
            argStr = ''
            docStr = tabs + ":param %s %s : %s " %(attrInfo['type'], attr, attrInfo['description'])
            if attrInfo['isDefaultSet'] == 'True':
                if isNumericAttr(attrInfo):
                    if attrInfo['isKey'] != 'True':
                        argStr = "\n" + spaces + "%s=%d," %(attr,int(attrInfo['default'].lstrip()))
                        assignmentStr = "int(%s)" %(attr)
                    else:
                        assignmentStr = "int(%s)" %(int(attrInfo['default'].lstrip()))
                elif isBoolean(attrInfo['type']):
                    if attrInfo['isKey'] != 'True':
                        argStr = "\n" + spaces + "%s=%s," %(attr, boolFromString(attrInfo['default'].lstrip()))
                        assignmentStr = "True if %s else False" %(attr)
                    else:
                        assignmentStr = "%s" %(boolFromString(attrInfo['default'].lstrip()))
                elif isListAttr(attrInfo):
                    if attrInfo['isKey'] != 'True':
                        argStr = "\n" + spaces + "%s=[]," %(attr)
                        assignmentStr = "%s" %(attr)
                    else:
                        assignmentStr = "'%s'" %(attrInfo['default'].lstrip())
                else:
                    if attrInfo['isKey'] != 'True':
                        argStr = "\n" + spaces + "%s=\'%s\'," %(attr,attrInfo['default'].lstrip())
                        assignmentStr = "%s" %(attr)
                    else:
                        assignmentStr = "'%s'" %(attrInfo['default'].lstrip())
            else:
                if isNumericAttr(attrInfo):
                    assignmentStr = "int(%s)" %(attr)
                elif isBoolean(attrInfo['type']):
                    assignmentStr = "True if %s else False" %(attr)
                else:
                    assignmentStr = "%s" %(attr)
                argStr = "\n" + spaces + "%s," %(attr)
                #docStr = docStr + "\t" + "%s : " %(attr)
            docLines.append(docStr +  attrInfo['description'] + "\n")

            lines.append(argStr)
            objLines.append(tabs+tabs + "\'%s\' : %s,\n" %(attr, assignmentStr))

        lines[-1] = lines[-1][0:lines[-1].find(',')]
        lines.append("):\n")
        objLines.append(tabs + tabs+"}\n")
        docLines.append("\n" + "\t\"\"\"" )
        lines = docLines + lines
        lines = lines + objLines
        lines.append (tabs + "reqUrl =  self.cfgUrlBase+" +"\'%s\'\n" %(self.name))
        lines.append(tabs + "r = requests.post(reqUrl, data=json.dumps(obj), headers=headers) \n")
        lines.append(tabs + "return r\n")
        fileHdl.writelines(lines)

    def createDeleteMethod(self, fileHdl):
        tabs = self.TAB
        #lines = [ "\n"+ tabs + "@processReturnCode"]
        lines = []
        lines.append("\n"+ tabs + "def delete" + self.name + "(self,")
        tabs = tabs + self.TAB
        spaces = ' ' * (len(lines[-1])  - len("self, "))
        objLines = [tabs + "obj =  { \n"]
        for (attr, attrInfo) in self.attrList:
            if attrInfo['isKey'] == 'True':
                lines.append("\n" + spaces + "%s," %(attr))
                objLines.append(tabs+tabs + "\'%s\' : %s,\n" %(attr, attr))
        lines[-1] = lines[-1][0:lines[-1].find(',')]
        lines.append("):\n")
        objLines.append(tabs + tabs+"}\n")
        lines = lines + objLines
        lines.append (tabs + "reqUrl =  self.cfgUrlBase+" +"\'%s\'\n" %(self.name))
        lines.append(tabs + "r = requests.delete(reqUrl, data=json.dumps(obj), headers=headers) \n")
        lines.append(tabs + "return r\n")
        fileHdl.writelines(lines)

    def createDeleteByIdMethod(self, fileHdl):
        tabs = self.TAB
        #lines = [ "\n"+ tabs + "@processReturnCode"]
        lines = []
        lines.append("\n"+ tabs + "def delete" + self.name + "ById(self, objectId ):\n")
        tabs = tabs + self.TAB
        lines.append (tabs + "reqUrl =  self.cfgUrlBase+" +"\'%s\'" %(self.name))
        lines[-1] = lines[-1] + "+\"/%s\"%(objectId)\n"
        lines.append(tabs + "r = requests.delete(reqUrl, data=None, headers=headers) \n")
        lines.append(tabs + "return r\n")
        fileHdl.writelines(lines)

    def createUpdateMethod (self, fileHdl):
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


    def createUpdateByIdMethod (self, fileHdl):
        tabs = self.TAB
        #lines = [ "\n"+ tabs + "@processReturnCode"]
        lines = []
        lines.append("\n"+ tabs + "def update" + self.name + "ById(self,\n")
        tabs = tabs + self.TAB
        spaces = ' ' * (len(lines[-1])  - len("self, "))
        lines.append(spaces+ "objectId,")
        objLines = [tabs + "obj =  {\'objectId\': objectId }\n"]
        for (attr, attrInfo) in self.attrList:
            if attrInfo['isKey'] != 'True':
                lines.append("\n" + spaces + "%s = None," %(attr))
                objLines.append(tabs + "if %s !=  None:\n" %(attr))
                objLines.append(tabs + self.TAB + "obj[\'%s\'] = %s\n\n" %(attr, attr))
        lines[-1] = lines[-1][0:lines[-1].find(',')]
        lines.append("):\n")
        lines = lines + objLines
        lines.append (tabs + "reqUrl =  self.cfgUrlBase+" +"\'%s\'\n" %(self.name))
        lines.append(tabs + "r = requests.patch(reqUrl, data=json.dumps(obj), headers=headers) \n")
        lines.append(tabs + "return r\n")                                                                                  
        fileHdl.writelines(lines)

    def createTblPrintMethod(self, fileHdl):
        pass

    def writeAllMethods (self, fileHdl):
        self.createCreateMethod(fileHdl)
        self.createUpdateMethod(fileHdl)
        self.createUpdateByIdMethod(fileHdl)
        self.createDeleteMethod(fileHdl)
        self.createDeleteByIdMethod(fileHdl)
        self.createGetMethod(fileHdl, 'self.cfgUrlBase')
        self.createGetByIdMethod(fileHdl)
        self.createGetAllMethod(fileHdl, 'self.cfgUrlBase')

