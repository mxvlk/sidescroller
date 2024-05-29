try:
    from unicorn_hat_sim import unicornhathd as uh # type: ignore
except ImportError:
    print("No unicorn hat sim!")


# displays the dev gui using the offical unicorn_hat_sim

def showUH(pixelArray: list, pixels):
    uh.rotation(270)
    uh.clear()
    for i in range(0, pixels):
        for j in range(0, pixels):
            uh.set_pixel(i, j, pixelArray[i][j][0],  pixelArray[i][j][1],  pixelArray[i][j][2])
    uh.show()