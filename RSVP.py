from psychopy import core, visual, event

win_width = 800
win_height = 600
win = visual.Window(size=[win_width, win_height], units='pix', fullscr=False)

# stim = visual.ShapeStim(win, units = 'pix', lineWidth = 50, lineColor = 'white', vertices = ((-200,200),(200,200), (200,-200), (-200,-200)), fillColor = pos = (0,0))

stim = visual.TextBox(window = win, text = 'test')
stim.draw()
win.flip()