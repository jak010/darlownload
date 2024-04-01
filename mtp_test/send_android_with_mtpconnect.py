import subprocess

binary_path = "/System/Volumes/Data/opt/homebrew/Cellar/libmtp/1.1.21/bin/"
mtp_connector = "mtp-connect"

options = ['--sendfile', './test.text', "/DCIM"]

subprocess.run([binary_path + mtp_connector] + options)
