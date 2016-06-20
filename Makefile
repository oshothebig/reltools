MKDIR=mkdir -p
RMDIRFORCE=rm -rf
PKG_BUILD=FALSE
PROD_NAME=flexswitch
BUILD_TARGET=cel_redstone
ifneq (,$(findstring $(PKG_BUILD), FALSE))
	EXT_INSTALL_PATH=
	BUILD_DIR=out
else
	EXT_INSTALL_PATH=/opt/$(PROD_NAME)
	BUILD_DIR=flexswitch-0.0.1
endif
ALL_DEPS=buildinfogen codegen installdir ipc exe install
SRCDIR=$(SR_CODE_BASE)/snaproute/src
DESTDIR=$(SR_CODE_BASE)/snaproute/src/$(BUILD_DIR)
ifneq (,$(findstring $(PKG_BUILD), FALSE))
	EXE_DIR=/bin
else
	EXE_DIR=
endif
COMPS=$(SR_CODE_BASE)/snaproute/src/asicd\
		$(SR_CODE_BASE)/snaproute/src/config\
		$(SR_CODE_BASE)/snaproute/src/infra\
		$(SR_CODE_BASE)/snaproute/src/l3\
		$(SR_CODE_BASE)/snaproute/src/l2\
		$(SR_CODE_BASE)/snaproute/src/flexSdk\
		$(SR_CODE_BASE)/snaproute/src/apps

COMPS_WITH_IPC=$(SR_CODE_BASE)/snaproute/src/asicd\
		$(SR_CODE_BASE)/snaproute/src/infra\
		$(SR_CODE_BASE)/snaproute/src/l3\
		$(SR_CODE_BASE)/snaproute/src/l2

define timedMake
@echo -n "Building component $(1) started at :`date`\n"
make -C $(1) exe DESTDIR=$(DESTDIR)/$(EXE_DIR) BUILD_TARGET=$(BUILD_TARGET) GOLDFLAGS="-r /opt/flexswitch/sharedlib";
@echo -n "Done building component $(1) at :`date`\n\n"
endef
all: $(ALL_DEPS)

installdir:
	$(MKDIR) $(DESTDIR)
	$(MKDIR) $(DESTDIR)/$(EXT_INSTALL_PATH)/
	$(MKDIR) $(DESTDIR)/$(EXT_INSTALL_PATH)/kmod
	$(MKDIR) $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	$(MKDIR) $(DESTDIR)/$(EXT_INSTALL_PATH)/models
	$(MKDIR) $(DESTDIR)/$(EXT_INSTALL_PATH)/params
	$(MKDIR) $(DESTDIR)/$(EXT_INSTALL_PATH)/sharedlib

.PHONY:buildinfogen
buildinfogen:
	echo 'Generating build information'
	$(shell python $(SR_CODE_BASE)/reltools/buildInfoGen.py)

codegen:
	$(SR_CODE_BASE)/reltools/codegentools/gencode.sh

codegenclean:
	$(SR_CODE_BASE)/reltools/codegentools/cleangencode.sh

exe: $(COMPS)
	@$(foreach f,$^, $(call timedMake, $(f)))

ipc: $(COMPS_WITH_IPC)
	$(foreach f,$^, make -C $(f) ipc DESTDIR=$(DESTDIR);)

copy: $(COMPS)
	$(foreach f,$^, make -C $(f) install DESTDIR=$(DESTDIR)/$(EXT_INSTALL_PATH) BUILD_TARGET=$(BUILD_TARGET);)

install:installdir copy
	install $(SR_CODE_BASE)/reltools/flexswitch $(DESTDIR)/$(EXT_INSTALL_PATH)
	install $(SR_CODE_BASE)/reltools/daemon.py $(DESTDIR)/$(EXT_INSTALL_PATH)
	install $(SR_CODE_BASE)/reltools/pkgInfo.json $(DESTDIR)/$(EXT_INSTALL_PATH)
	install $(SR_CODE_BASE)/reltools/buildInfo.json $(DESTDIR)/$(EXT_INSTALL_PATH)
	install $(SRCDIR)/models/events/events.json $(DESTDIR)/$(EXT_INSTALL_PATH)
	install $(SRCDIR)/models/events/asicdEvents.json $(DESTDIR)/$(EXT_INSTALL_PATH)
	install $(SRCDIR)/models/events/arpdEvents.json $(DESTDIR)/$(EXT_INSTALL_PATH)
ifeq (,$(findstring $(PKG_BUILD), FALSE))
	install $(SRCDIR)/$(BUILD_DIR)/confd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/arpd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/fMgrd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/dhcpd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/bgpd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/ospfd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/ribd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/asicd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/dhcprelayd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/lacpd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/stpd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/bfdd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/vrrpd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/sysd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/lldpd $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
	install $(SRCDIR)/$(BUILD_DIR)/vxland $(DESTDIR)/$(EXT_INSTALL_PATH)/bin
endif
	install $(SR_CODE_BASE)/reltools/codegentools/._genInfo/*.json  $(DESTDIR)/$(EXT_INSTALL_PATH)/models/
	install $(SRCDIR)/models/objects/genObjectConfig.json  $(DESTDIR)/$(EXT_INSTALL_PATH)/models/
	install $(SR_CODE_BASE)/external/src/github.com/nanomsg/nanomsg/.libs/libnanomsg.so.4.0.0 $(DESTDIR)/$(EXT_INSTALL_PATH)/sharedlib

clean: $(COMPS)
	$(SR_CODE_BASE)/reltools/codegentools/cleangencode.sh
	$(foreach f,$^, make -C $(f) clean;)
	$(RMDIRFORCE) $(DESTDIR)
