# Handout-only challenge: no build or server, just the binary players download
# (served from publish/ at /files/...).
#
# warp (17 MB) is kept xz-compressed in git; publishing decompresses it so
# players download the binary itself. A pre-compressed warp.gz is published
# next to it: the web server serves it transparently (Content-Encoding: gzip)
# to clients that accept gzip, cutting the transfer to ~4 MB while the browser
# still saves a plain `warp`.
$(BUILD_DIR)/warp: $(DIR)/attachments/warp.xz
	$(_V)echo "Unpacking $(@F)"
	$(_v)mkdir -p $(@D) && xz -dc $< > $@

$(BUILD_DIR)/warp.gz: $(BUILD_DIR)/warp
	$(_V)echo "Pre-compressing $(@F) for the web server"
	$(_v)gzip -9n -c $< > $@

PUBLISH_BUILD := warp warp.gz
