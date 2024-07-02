include $(TOPDIR)/rules.mk

PKG_NAME:=sniff7
PKG_VERSION:=0.0.1
PKG_RELEASE:=1

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk


define Package/sniff7
  SECTION:=net
  CATEGORY:=Network
  TITLE:=Field 7 Sniffer
  DEPENDS:=+libpcap +libpthread +libcurl +libprotobuf-c
endef


define Package/sniff7/description
  Field 7 Sniffer.
endef


define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef


TARGET_CFLAGS += -Wall -Werror -O2
TARGET_LIBS =-Wl,-Bstatic -lpcap \
			 -Wl,-Bdynamic -lpthread \
			 -Wl,-Bstatic -lcurl \
			 -Wl,-Bstatic -lprotobuf-c \
			 -Wl,-Bdynamic -lgcc_s
			 

define Build/Compile
	$(TARGET_CONFIGURE_OPTS) \
	CFLAGS="$(TARGET_CFLAGS)" \
	LDFLAGS="$(TARGET_LDFLAGS) -Wl,--verbose=99" \
	LIBS="$(TARGET_LIBS)" \
	$(MAKE) -C $(PKG_BUILD_DIR)
endef

define Package/sniff7/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/sniff7 $(1)/usr/sbin/
endef

$(eval $(call BuildPackage,sniff7))
