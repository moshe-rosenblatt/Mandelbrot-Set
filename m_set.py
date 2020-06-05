import cmath, image, sys, numpy, time

def grid(pixel, zoom, up, left, name):
    ''' Create a grid of complex number as a list '''

    print (f"{name}_{zoom}_{up}_{left}.png")

    # sets the size and boundaries of the grid
    boarder_x = (-2.5/zoom, 1/zoom)
    boarder_y = (-1/zoom, 1/zoom)
    resolution_x = 35*pixel
    resolution_y = 20*pixel
    # sets the jumps between pixels
    (x, y) = ([], [])
    jamps_x = (boarder_x[1]-boarder_x[0])/resolution_x
    jamps_y = (boarder_y[1]-boarder_y[0])/resolution_y
    # creates a grid with the jumps
    for i in range(resolution_x):
        x.extend([boarder_x[0]+(i*jamps_x)+left])
    for i in range(resolution_y):
        y.extend([boarder_y[0]+(i*jamps_y)+up])
    # changes grid with complex number
    board = []
    for i in y:
        for n in x:
            board.extend([complex(n, i)])
    print ("grid created")
    return (board, resolution_x)

def calculation (board, power):
    '''calculate the The Mandelbrot Set- \n
    takes a list of complex number and return \n
    a list with the number of time it was squared for each complex number '''
    new_board = []
    pix_checked = 0
    start_time = time.time()

    # iterating over the numbers in the board
    for i in board:
        u = 0
        c = complex(0, 0)
        pix_checked += 1
        while True:
            # squares the number and adds it to  itself
            c = pow(c, 2) + i
            u += 1
            # checks if the number is out of range
            if cmath.polar(c)[0] >2:
                new_board.extend([u])
                break
            # checks if the number is still inside the set
            if u > (power*255):
                new_board.extend([0])
                break

        # printing the progress
        progress = (pix_checked/len(board))*100
        if progress % 1 == 0:
            estimated_time = (time.time() - start_time)*((100/progress)-1)
            print(f"progress {progress} % , {pix_checked} pixels , {cloke(estimated_time)} Seconds remaining " , end="\r")

    return new_board

def img_create (board, resolution, name, name1, name2, name3, power, print_tipe, color):
    ''' Taking the square board and output it as a png file or in a window '''

    # define the image parameters
    height = int(resolution//1.75)
    width = int(resolution)
    if (print_tipe==1): win = image.ImageWin(width, height) 
    img = image.EmptyImage(width, height)

    # iterating over the pixels in the img
    counter = 0
    for row in range(height):
        for col in range(width):
            # sets the color black if the value is 0
            if board[counter] == 0:
                this_pixel = image.Pixel(0, 0, 0)
            else:
                # checks if color is required 
                if (color == 0):
                    # sets the colors according to the value
                    (red, green, blue) = colors(board[counter])
                    this_pixel = image.Pixel(red, green, blue)
                else:
                    # sets thhe gray levels according to the value
                    pix_val = board[counter]//power
                    this_pixel = image.Pixel(pix_val, pix_val, pix_val)
            img.set_pixel(col, row, this_pixel)
            counter += 1
    
    if (print_tipe==1):
        img.draw(win)
        print(''); input()
    else:
        img.save(f'{name}_{name1}_{name2}_{name3}.png')

def colors (x):
    '''replaces a square number with three color values '''
    x = x/500
    red = (numpy.sin(2*numpy.pi*x-1.5)+1)*128
    green = (numpy.sin(2*numpy.pi*x)+1)*128
    blue = (numpy.cos(2*numpy.pi*x)+1)*128
    

    return red, green, blue

def cloke (secend):
    '''Take secends and return them in a hh:mm:ss format'''
    s = int(secend)
    secend = str(    s % 60    ).zfill(2)
    minute = str( (s//60) % 60 ).zfill(2)
    hour =   str( s  //  3600  ).zfill(2)
    return (f"{hour}:{minute}:{secend} ")

def m_help ():

    print(
    ''''A list of the variables and the values that can be used in the program: 
        
    r-   (5-50)   resolution of the imeg,             default is 5 
    z-   (1-...)  zoom in the set,                    default is 1 
    u-   (-2--2)  amount of shifting upward ,         default is 0 
    l-   (-2--2)  amount of shifting leftward ,       default is 0 
    na-  ('')     the name of the file,               default is \"un_title\"
    po-  (1-64)   times of squared (1=255),           default is 2
    pt-  (0/1)    print tipe (0-img/ 1-win),          default is 0 (img) 
    co-  (0/1)    colors (0-colors / 1-b&w),          default is 0 (colors)
    lo-           loop creates multiple images
                  it need two variables to work:
                  1- is the amount of images
                  2- is the size of the jumps in the zoom between images
    \n Example:
    m_set.py na- tt
    m_set.py na- test z- 90 u- 0.098 l- -0.747 po- 4 r- 15 lo 2 1.5 '''
    )

def main ():
    '''the main program sequence'''
    # pixel, zoom, up, left, power, print_tipe, color, name
    
    if len(sys.argv)==1 : m_help()

    else:

        #setting the default parameters
        name, pixel, zoom, up, left = 'un_title', 5, 1, 0.0, 0.0
        power, print_tipe, color, loopn, loopj = 2, 0, 0, 1, 0

        try:
            # looping in to the argv to reset the parameters
            for arg in range(1, len(sys.argv)-1):
                come, value = sys.argv[arg], sys.argv[arg+1]
                if   come == 'r-':   pixel=int(value)
                elif come == 'z-':   zoom=float(value)
                elif come == 'u-':   up=float(value)
                elif come == 'l-':   left=float(value)
                elif come == 'po-':  power=int(value)
                elif come == 'pt-':  print_tipe=int(value)
                elif come == 'co-':  color=int(value)
                elif come == 'na-':  name=value
                elif come == 'lo-':  loopn, loopj =int(value), float(sys.argv[arg+2])
                

            loopc = loopn
            while (loopc >= 1):
                if (loopn!=1 ): print (f'\n\nimage {loopn-loopc+1}/{loopn}')
                (board, resolution) = grid (pixel, zoom , up , left, name)
                img_create(calculation(board, power), resolution, name, zoom, up ,left, power, print_tipe, color)
                zoom = zoom*loopj
                loopc -= 1
     
        except :
            print('One or more of the variables or values is incorrect')

  
if __name__ == "__main__":

    main()

