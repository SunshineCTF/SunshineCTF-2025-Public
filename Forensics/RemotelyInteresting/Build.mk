# Handout-only challenge: no build or server, just the memory dump players
# download (served from publish/ at /files/...).
#
# dmp.7z is 157 MB, so it is split into parts under 50 MB to fit in git; the
# parts are joined here at publish time and the whole dmp.7z is published.
REMOTELYINTERESTING_PARTS := $(sort $(wildcard $(DIR)/attachments/dmp.7z.part-*))

$(BUILD_DIR)/dmp.7z: $(REMOTELYINTERESTING_PARTS)
	$(_V)echo "Joining $(@F) from $(words $^) parts"
	$(_v)mkdir -p $(@D) && cat $^ > $@

PUBLISH_BUILD := dmp.7z
