-
settings():
    user.window_snap_screen = 'size aware'

key(shift-alt-ctrl-cmd-p):
    user.move_window_next_screen()

key(shift-ctrl-alt-cmd-t): user.snap_window(user.translate_snap_name('full'))
key(shift-ctrl-alt-cmd-s): user.snap_window(user.translate_snap_name('left'))
key(shift-ctrl-alt-cmd-d): user.snap_window(user.translate_snap_name('right'))

key(shift-ctrl-alt-cmd-q): user.layout_video_call_windows("one_on_one")
key(shift-ctrl-alt-cmd-a): user.layout_video_call_windows("gallery")
key(shift-ctrl-alt-cmd-z): user.layout_video_call_windows("screenshare")

key(shift-ctrl-alt-cmd-x): user.layout_all_windows()
