-
key(shift-alt-ctrl-cmd-1):
  user.just_activate_n("Emacs")

key(shift-alt-ctrl-cmd-2):
  user.just_activate("/Applications/Arc.app")

key(shift-alt-ctrl-cmd-3):
  user.just_activate("/Applications/iTerm.app")

key(shift-alt-ctrl-cmd-4):
  user.just_activate("/Applications/Slack.app")

key(shift-alt-ctrl-cmd-5):
  user.just_activate_and_key("/Applications/Mimestream.app", "cmd-0")

key(shift-alt-ctrl-cmd-6):
  user.just_activate_preferred("/System/Applications/FaceTime.app", "/Applications/zoom.us.app")

key(shift-alt-ctrl-cmd-7):
  user.just_activate("/Applications/Element.app")

key(shift-alt-ctrl-cmd-8):
  user.launch_and_activate("/System/Applications/Messages.app")

key(shift-alt-ctrl-cmd-9):
  user.launch_and_activate("/Applications/BusyCal.app")

key(shift-alt-ctrl-cmd-0):
  user.launch_and_activate("/Applications/Obsidian.app")

# Dash needs the shortcut alt-ctrl-cmd-space defined:
key(f18): key(alt-ctrl-cmd-space)

key(f19): user.toggle_active_app("/Applications/LaunchBar.app")
