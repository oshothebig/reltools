#!/usr/bin/env python
import os
import sys
from optparse import OptionParser

#Global variables
srBase = os.environ.get('SR_CODE_BASE', None)
srCodeBase = ""
daemonDirectory = ""
rpcDirectory = ""
serverDirectory = ""
repoName = ""
moduleName = ""
daemonName = ""

#Create directory structure for the new daemon
def createDirectoryStructure(dmnName, modName, rName, baseDir):
    global daemonDirectory, rpcDirectory, serverDirectory, repoName, moduleName, daemonName
    daemonDirectory = baseDir + rName + "/" + dmnName + "/"
    rpcDirectory = daemonDirectory + "rpc/"
    serverDirectory = daemonDirectory + "server/"
    repoName = rName
    moduleName = modName
    daemonName = dmnName

    if not os.path.exists(daemonDirectory):
        os.makedirs(daemonDirectory)
    else:
        print(daemonDirectory, "exists")

    if not os.path.exists(rpcDirectory):
        os.makedirs(rpcDirectory)
    else:
        print(rpcDirectory, "exists")

    if not os.path.exists(serverDirectory):
        os.makedirs(serverDirectory)
    else:
        print(serverDirectory, "exists")


def writeMainFile():
    global daemonDirectory, repoName, daemonName, moduleName
    fileName = daemonDirectory + "main.go"
    mainfd = open(fileName, 'w+')
    mainfd.write("""//
//Copyright [2016] [SnapRoute Inc]
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
//       Unless required by applicable law or agreed to in writing, software
//       distributed under the License is distributed on an "AS IS" BASIS,
//       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//       See the License for the specific language governing permissions and
//       limitations under the License.
//
//   This is a auto-generated file, please do not edit!
// _______   __       __________   ___      _______.____    __    ____  __  .___________.  ______  __    __ 
// |   ____||  |     |   ____\  \ /  /     /       |\   \  /  \  /   / |  | |           | /      ||  |  |  |
// |  |__   |  |     |  |__   \  V  /     |   (----  \   \/    \/   /  |  |  ---|  |----    ,---- |  |__|  |
// |   __|  |  |     |   __|   >   <       \   \      \            /   |  |     |  |        |     |   __   |
// |  |     |  `----.|  |____ /  .  \  .----)   |      \    /\    /    |  |     |  |        `----.|  |  |  |
// |__|     |_______||_______/__/ \__\ |_______/        \__/  \__/     |__|     |__|      \______||__|  |__|
//\n""")
    mainfd.write("package main\n\n")
    if repoName == "":
        rpcImport = moduleName + "/rpc"
        serverImport = moduleName + "/server"
    else:
        rpcImport = repoName + "/" + moduleName + "/rpc"
        serverImport = repoName + "/" + moduleName + "/server"
    mainfd.write("""import (\n    "%s"\n    "%s"\n    "strconv"\n    "strings"\n    "utils/dmnBase"\n)\n\n""" % (rpcImport, serverImport))
    mainfd.write("""const (\n DMN_NAME = "%s"\n)\n\n""" % daemonName)
    mainfd.write("type Daemon struct {\n   *dmnBase.FSBaseDmn\n    daemonServer *server.DmnServer\n    rpcServer *rpc.RPCServer\n}\n\n")
    mainfd.write("var dmn Daemon\n\n")
    mainfd.write("""func main() {
        dmn.FSBaseDmn = dmnBase.NewBaseDmn(DMN_NAME, DMN_NAME)
        ok := dmn.Init()
        if !ok {
                panic("Daemon Base initialization failed for %s")
        }

        serverInitParams := &server.ServerInitParams{
                DmnName:   DMN_NAME,
                ParamsDir: dmn.ParamsDir,
                DbHdl:     dmn.DbHdl,
                Logger:    dmn.FSBaseDmn.Logger,
        }
        dmn.daemonServer = server.New%sServer(serverInitParams)
        go dmn.daemonServer.Serve()

        var rpcServerAddr string
        for _, value := range dmn.FSBaseDmn.ClientsList {
                if value.Name == strings.ToLower(DMN_NAME) {
                        rpcServerAddr = "localhost:" + strconv.Itoa(value.Port)
                        break
                }
        }
        if rpcServerAddr == "" {
                panic("Daemon %s is not part of the system profile")
        }
        dmn.rpcServer = rpc.NewRPCServer(rpcServerAddr, dmn.FSBaseDmn.Logger)

        dmn.StartKeepAlive()

        // Wait for server started msg before opening up RPC port to accept calls
        _ = <-dmn.daemonServer.InitCompleteCh

        //Start RPC server
        dmn.FSBaseDmn.Logger.Info("Daemon Server started for %s")
        dmn.rpcServer.Serve()
        panic("Daemon RPC Server terminated %s")
}\n""" % (daemonName, daemonName.upper(), daemonName, daemonName, daemonName))
    mainfd.close()


def writeRpcFile():
    global rpcDirectory, daemonName
    fileName = rpcDirectory + "rpc.go"
    rpcfd = open(fileName, 'w+')
    rpcfd.write("""//
//Copyright [2016] [SnapRoute Inc]
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
//       Unless required by applicable law or agreed to in writing, software
//       distributed under the License is distributed on an "AS IS" BASIS,
//       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//       See the License for the specific language governing permissions and
//       limitations under the License.
//
//   This is a auto-generated file, please do not edit!
// _______   __       __________   ___      _______.____    __    ____  __  .___________.  ______  __    __ 
// |   ____||  |     |   ____\  \ /  /     /       |\   \  /  \  /   / |  | |           | /      ||  |  |  |
// |  |__   |  |     |  |__   \  V  /     |   (----  \   \/    \/   /  |  |  ---|  |----    ,---- |  |__|  |
// |   __|  |  |     |   __|   >   <       \   \      \            /   |  |     |  |        |     |   __   |
// |  |     |  `----.|  |____ /  .  \  .----)   |      \    /\    /    |  |     |  |        `----.|  |  |  |
// |__|     |_______||_______/__/ \__\ |_______/        \__/  \__/     |__|     |__|      \______||__|  |__|
//\n""")
    rpcfd.write("package rpc\n\n")
    rpcfd.write("""import (\n    "%s"\n    "git.apache.org/thrift.git/lib/go/thrift"\n    "utils/logging"\n)\n\n""" % daemonName)
    rpcfd.write("type rpcServiceHandler struct {\n    logger logging.LoggerIntf\n}\n\n")
    rpcfd.write("func newRPCServiceHandler(logger logging.LoggerIntf) *rpcServiceHandler {\n    return &rpcServiceHandler{\n        logger: logger,\n    }\n}\n\n")
    rpcfd.write("type RPCServer struct {\n    *thrift.TSimpleServer\n}\n\n")
    rpcfd.write("""func NewRPCServer(rpcAddr string, logger logging.LoggerIntf) *RPCServer {
        transport, err := thrift.NewTServerSocket(rpcAddr)
        if err != nil {
                panic(err)
        }
        handler := newRPCServiceHandler(logger)
        processor := exampled.New%sServicesProcessor(handler)
        transportFactory := thrift.NewTBufferedTransportFactory(8192)
        protocolFactory := thrift.NewTBinaryProtocolFactoryDefault()
        server := thrift.NewTSimpleServer4(processor, transport, transportFactory, protocolFactory)
        return &RPCServer{
                TSimpleServer: server,
        }
}\n""" % daemonName.upper())
    rpcfd.close()


def writeServerFile():
    global serverDirectory, daemonName
    fileName = serverDirectory + "server.go"
    serverfd = open(fileName, 'w+')
    serverfd.write("""//
//Copyright [2016] [SnapRoute Inc]
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
//       Unless required by applicable law or agreed to in writing, software
//       distributed under the License is distributed on an "AS IS" BASIS,
//       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//       See the License for the specific language governing permissions and
//       limitations under the License.
//
//   This is a auto-generated file, please do not edit!
// _______   __       __________   ___      _______.____    __    ____  __  .___________.  ______  __    __ 
// |   ____||  |     |   ____\  \ /  /     /       |\   \  /  \  /   / |  | |           | /      ||  |  |  |
// |  |__   |  |     |  |__   \  V  /     |   (----  \   \/    \/   /  |  |  ---|  |----    ,---- |  |__|  |
// |   __|  |  |     |   __|   >   <       \   \      \            /   |  |     |  |        |     |   __   |
// |  |     |  `----.|  |____ /  .  \  .----)   |      \    /\    /    |  |     |  |        `----.|  |  |  |
// |__|     |_______||_______/__/ \__\ |_______/        \__/  \__/     |__|     |__|      \______||__|  |__|
//\n""")
    serverfd.write("package server\n\n")
    serverfd.write("""import (
        "time"
        "utils/dbutils"
        "utils/logging"
)\n\n""")
    serverfd.write("""type DmnServer struct {
        // store info related to server
        DbHdl          dbutils.DBIntf
        Logger         logging.LoggerIntf
        InitCompleteCh chan bool
}\n\n""")
    serverfd.write("""type ServerInitParams struct {
        DmnName     string
        ParamsDir   string
        CfgFileName string
        DbHdl       dbutils.DBIntf
        Logger      logging.LoggerIntf
}\n\n""")
    serverfd.write("""func New%sServer(initParams *ServerInitParams) *DmnServer {
        srvr := DmnServer{}
        srvr.DbHdl = initParams.DbHdl
        srvr.Logger = initParams.Logger
        srvr.InitCompleteCh = make(chan bool)

        // setup whatever you need for your server

        return &srvr
}\n\n""" % daemonName.upper())
    serverfd.write("""func (srvr *DmnServer) Serve() {
        srvr.Logger.Info("Server initialization started")
        //err := srvr.initServer()
        //if err != nil {
        //      panic(err)
        //}
        srvr.InitCompleteCh <- true
        srvr.Logger.Info("Server initialization complete, starting cfg/state listerner")
        for {
                //select {
                //case req := <-srvr.ReqChan:
                //      srvr.Logger.Info("Server request received - ", *req)
                //      srvr.handleRPCRequest(req)

                //}
                time.Sleep(30 * time.Second)
        }
}\n""")
    serverfd.close()


def writeMakeFile():
    global daemonDirectory, daemonName, repoName
    fileName = daemonDirectory + "Makefile"
    mkfd = open(fileName, 'w+')
    mkfd.write("""RM=rm -f
RMFORCE=rm -rf
DESTDIR=$(SR_CODE_BASE)/snaproute/src/out/bin
GENERATED_IPC=$(SR_CODE_BASE)/generated/src
IPC_GEN_CMD=thrift
SRCS=main.go
IPC_SRCS=rpc/%s.thrift
COMP_NAME=%s
GOLDFLAGS=-r /opt/flexswitch/sharedlib
all:exe
all:ipc exe
ipc: $(IPC_GEN_CMD) -r --gen go -out $(GENERATED_IPC) $(IPC_SRCS)

exe: $(SRCS)
        go build -o $(DESTDIR)/$(COMP_NAME) -ldflags="$(GOLDFLAGS)" $(SRCS)
 
guard:
ifndef SR_CODE_BASE 
        $(error SR_CODE_BASE is not set)
endif

install: @echo "%s has no files to install"
clean:guard
        $(RM) $(DESTDIR)/$(COMP_NAME) 
        $(RMFORCE) $(GENERATED_IPC)/$(COMP_NAME)\n""" % (daemonName, daemonName, daemonName))


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-d", "--daemon",
                      dest="daemon",
                      action="store",
                      help="Name of the daemon")

    parser.add_option("-m", "--module",
                      dest="module",
                      action="store",
                      help="Name of the module")

    parser.add_option("-r", "--repo",
                      dest="repo",
                      action="store",
                      help="Name of the repo this demon belongs to")

    if srBase[len(srBase)-1] != '/':
        srBase = srBase + "/"
    srCodeBase = srBase + "snaproute/src/"

    (opts, args) = parser.parse_args()

    if opts.daemon == None:
        parser.print_usage()
        sys.exit(0)
    else:
        dmnName = opts.daemon

    if opts.module != None:
        modName = opts.module
    else:
        modName = dmnName[:-1]

    if opts.repo != None:
        rName = opts.repo
    else:
        rName = ""

    createDirectoryStructure(dmnName, modName, rName, srCodeBase)
    writeMainFile()
    writeRpcFile()
    writeServerFile()
    writeMakeFile()
