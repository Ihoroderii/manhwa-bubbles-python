import cairo 

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 400)
ctx = cairo.Context(surface)
ctx.set_source_rgb(1,1,1)
ctx.paint()




surface.write_to_png("my_test_one.png")