import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from Map import Map

def vis1():
    # Make an array with ones in the shape of an 'X'
    a = np.eye(10,10)
    a += a[::-1,:]
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    # Bilinear interpolation - this will look blurry
    ax1.imshow(a, cmap=cm.Greys_r)
    ax2 = fig.add_subplot(122)
    # 'nearest' interpolation - faithful but blocky
    ax2.imshow(a, interpolation='nearest', cmap=cm.Greys_r)
    plt.show()

def vis2():
    np.random.seed(19680801)
    Nr = 3
    Nc = 2
    cmap = "cool"
    fig, axs = plt.subplots(Nr, Nc)
    fig.suptitle('Multiple images')
    images = []
    for i in range(Nr):
        for j in range(Nc):
            # Generate data with a range that varies from one plot to the next.
            data = ((1 + i + j) / 10) * np.random.rand(10, 20) * 1e-6
            images.append(axs[i, j].imshow(data, cmap=cmap))
            axs[i, j].label_outer()
    # Find the min and max of all colors for use in setting the color scale.
    vmin = min(image.get_array().min() for image in images)
    vmax = max(image.get_array().max() for image in images)
    norm = colors.Normalize(vmin=vmin, vmax=vmax)
    for im in images:
        im.set_norm(norm)
    fig.colorbar(images[0], ax=axs, orientation='horizontal', fraction=.1)
    # Make images respond to changes in the norm of other images (e.g. via the
    # "edit axis, curves and images parameters" GUI on Qt), but be careful not to
    # recurse infinitely!
    def update(changed_image):
        for im in images:
            if (changed_image.get_cmap() != im.get_cmap()
                    or changed_image.get_clim() != im.get_clim()):
                im.set_cmap(changed_image.get_cmap())
                im.set_clim(changed_image.get_clim())

    for im in images:
        im.callbacksSM.connect('changed', update)
    plt.show()

def vis3():
    methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
               'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
               'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    grid = np.random.rand(4, 4)
    fig, axs = plt.subplots(nrows=3, ncols=6, figsize=(9.3, 6),
                            subplot_kw={'xticks': [], 'yticks': []})
    fig.subplots_adjust(left=0.03, right=0.97, hspace=0.3, wspace=0.05)
    for ax, interp_method in zip(axs.flat, methods):
        ax.imshow(grid, interpolation=interp_method, cmap='viridis')
        ax.set_title(str(interp_method))
    plt.tight_layout()
    plt.show()

def vis4():
    harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0, 1, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0, 2, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0, 3, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0, 4, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1, 5, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3, 6, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0, 7, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0]])


    fig, ax = plt.subplots()
    im = ax.imshow(harvest)

    # We want to show all ticks...


    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(14):
        for j in range(14):
            text = ax.text(j, i, harvest[i, j],
                           ha="center", va="center", color="w")

    ax.set_title("Autonomous Robot Path")
    fig.tight_layout()
    plt.show()

#vis4()
p1 = Map()
npMap = p1.getNpMap()
#p1.printNpMap()

harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0, 1, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0, 2, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0, 3, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0, 4, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1, 5, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3, 6, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0, 7, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3, 0, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0]])

state1 = np.zeros((10, 10))
state1[5, 5] = 4
state1[5, 6] = 1

state1[4, 5] = 4
state1[4, 6] = 1

state2 = np.zeros((10, 10))
state2[5, 5] = 2
state2[5, 6] = 2
state2[5, 7] = 2
state2[5, 8] = 2
state2[5, 9] = 3
state2[6, 8] = 4
state2[7, 8] = 1

state2[4, 5] = 2
state2[4, 6] = 2
state2[4, 7] = 3
state2[3, 6] = 2
state2[2, 6] = 2
state2[1, 6] = 4
state2[0, 6] = 3

state3 = np.zeros((10, 10))
state3[5, 5] = 2
state3[5, 6] = 2
state3[5, 7] = 2
state3[5, 8] = 2
state3[5, 9] = 3
state3[6, 8] = 2
state3[7, 8] = 2
state3[8, 8] = 2
state3[9, 8] = 3
state3[8, 7] = 2
state3[8, 6] = 4
state3[8, 5] = 1

state3[1, 6] = 2
state3[4, 5] = 2
state3[4, 6] = 2
state3[4, 7] = 3
state3[3, 6] = 2
state3[2, 6] = 2
state3[1, 6] = 2
state3[0, 6] = 3
state3[1, 7] = 2
state3[1, 8] = 2
state3[1, 9] = 3
state3[2, 7] = 4
state3[3, 8] = 3
state3[2, 8] = 2

state4 = np.zeros((10, 10))
state4[5, 5] = 2
state4[5, 6] = 2
state4[5, 7] = 2
state4[5, 8] = 2
state4[5, 9] = 3
state4[6, 8] = 2
state4[7, 8] = 2
state4[8, 8] = 2
state4[9, 8] = 3
state4[8, 7] = 2
state4[8, 6] = 4
state4[8, 5] = 1

state4[1, 6] = 2
state4[4, 5] = 2
state4[4, 6] = 2
state4[4, 7] = 3
state4[3, 6] = 2
state4[2, 6] = 2
state4[1, 6] = 2
state4[0, 6] = 3
state4[1, 7] = 2
state4[1, 8] = 2
state4[1, 9] = 3
state4[2, 7] = 4
state4[3, 8] = 3
state4[2, 8] = 2

state5 = np.zeros((10, 10))

state5[5, 5] = 2
state5[5, 6] = 2
state5[5, 7] = 2
state5[5, 8] = 2
state5[5, 9] = 3
state5[6, 8] = 2
state5[7, 8] = 2
state5[8, 8] = 2
state5[9, 8] = 3
state5[8, 7] = 2
state5[8, 6] = 2
state5[8, 5] = 2
state5[8, 4] = 2
state5[8, 3] = 2
state5[8, 2] = 2
state5[8, 1] = 4
state5[8, 0] = 3

state5[1, 6] = 2
state5[4, 5] = 2
state5[4, 6] = 2
state5[4, 7] = 3
state5[3, 6] = 2
state5[2, 6] = 2
state5[1, 6] = 2
state5[0, 6] = 3
state5[1, 7] = 2
state5[1, 8] = 2
state5[1, 9] = 3
state5[2, 7] = 2
state5[3, 8] = 3
state5[2, 8] = 2
state5[2, 5] = 2
state5[2, 4] = 2
state5[2, 3] = 2
state5[2, 2] = 4
state5[2, 1] = 1

state6 = np.zeros((10, 10))
state6.fill(2)

state6[0, 0] = 3
state6[0, 1] = 3
state6[0, 2] = 3
state6[0, 3] = 3
state6[0, 4] = 3
state6[0, 5] = 3
state6[0, 6] = 3
state6[0, 7] = 3
state6[0, 8] = 3
state6[0, 9] = 3

state6[0, 0] = 3
state6[1, 0] = 3
state6[2, 0] = 3
state6[3, 0] = 3
state6[4, 0] = 3
state6[5, 0] = 3
state6[6, 0] = 3
state6[7, 0] = 3
state6[8, 0] = 3
state6[9, 0] = 3

state6[9, 0] = 3
state6[9, 1] = 3
state6[9, 2] = 3
state6[9, 3] = 3
state6[9, 4] = 3
state6[9, 5] = 3
state6[9, 6] = 3
state6[9, 7] = 3
state6[9, 8] = 3
state6[9, 9] = 3

state6[0, 9] = 3
state6[1, 9] = 3
state6[2, 9] = 3
state6[3, 9] = 3
state6[4, 9] = 3
state6[5, 9] = 3
state6[6, 9] = 3
state6[7, 9] = 3
state6[8, 9] = 3
state6[9, 9] = 3

state6[8, 8] = 0
state6[8, 7] = 1
state6[8, 6] = 4

state6[4, 5] = 4

state6[4, 7] = 3
state6[3, 7] = 3
state6[4, 8] = 3
state6[3, 8] = 3

state6[7, 2] = 3
state6[6, 2] = 3

state6[1, 2] = 3
state6[1, 3] = 3
state6[1, 4] = 3

# 0 undetected, 1 untraveled, 3 obstacle, 2 traveled, 4 robot position



fig, ax = plt.subplots()
im = ax.imshow(state6)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

for i in range(10):
    for j in range(10):
        text = ax.text(j, i, state6[i, j],
                        ha="center", va="center", color="w")

ax.set_title("Autonomous Robot Path")
fig.tight_layout()
plt.show()
