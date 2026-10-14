# Handout-only challenge: no build or server, just the binary players download
# (served from publish/ at /files/...).
#
# warp (17 MB) is kept xz-compressed in git; publishing decompresses it so
# players download the binary itself (the web server compresses in transit).
$(BUILD_DIR)/warp: $(DIR)/attachments/warp.xz
	$(_V)echo "Unpacking $(@F)"
	$(_v)mkdir -p $(@D) && xz -dc $< > $@

PUBLISH_BUILD := warp
