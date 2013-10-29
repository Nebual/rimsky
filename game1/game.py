import pyglet
import physicalobject

game_window = pyglet.window.Window(800, 600)
main_batch = pyglet.graphics.Batch()

text1 = pyglet.text.Label(text="some text", x=400, y=300, anchor_x="center", batch=main_batch)
player_ship = physicalobject.Player(x=400, y=200, batch=main_batch)
game_window.push_handlers(player_ship.key_handler)


def update(dt):
	player_ship.update(dt)
	
@game_window.event
def on_draw():
	game_window.clear()
	main_batch.draw()
	
if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()
