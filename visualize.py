import gc
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation, PillowWriter
from genetic_alg import Population
import numpy as np
import pandas as pd


with plt.style.context(("ggplot", "seaborn")):
    fig = plt.figure(constrained_layout=True, figsize=(16, 9))
    specs = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)

    main = fig.add_subplot(specs[0, 0])
    curve = fig.add_subplot(specs[1, 0])
    top = fig.add_subplot(specs[0, 1])
    bottom = fig.add_subplot(specs[1, 1])

    s_poss = np.logspace(-14, -2, 200)
    t_poss = np.logspace(-3, 3, 100)
    s_poss2 = np.logspace(-4.3, -4.4, 200)
    t_poss2 = np.logspace(.7, .78, 100)
    # y = np.load("./data/s-valus.npy")
    # x = np.load("./data/t-values.npy")
    e = np.load("./data/field.npy")
    e2 = np.load("./data/field-zoom.npy")

    imgplot = main.pcolor(s_poss,t_poss,e, cmap='gist_rainbow', shading='auto')
    imgplot2 = top.pcolor(s_poss2,t_poss2,e2, cmap='gist_rainbow', shading='auto')
    # imgplot.set_cmap('nipy_spectral')
    population_plt = main.scatter(range(100), range(100), c=['red']*10+['black']*90, s = 8)
    zoom_plt = top.scatter(range(100), range(100), c=range(100), cmap='gray', alpha=0.7)
    err_plts = [bottom.plot(range(100),
                            range(100),
                            linewidth=2.5-0.2*i,
                            alpha=0.5,
                            color='red')[0]
                for i in range(10)]

    main.set_title("Original Sample Range")
    top.set_title("Solution Range")
    bottom.set_title("Error")
    # top.legend((success_plt, talent_plt, luck_plt),
    #            ("Success", "Talent", "Luck"))

    # bleft_bar = bleft.bar(range(args.choose+1), freq_table, color="tab:blue")
    # bleft.set_ylabel('Frequency of Occurance')
    # bleft.set_xlabel("How many of them would be on top without luck")
    # bleft.set_title('This Batch')

    # bright_bar = bright.bar(range(args.choose+1), whole_data, color="tab:blue")
    # bright.set_ylabel('Frequency of Occurance')
    # bright.set_xlabel("How many of them would be on top without luck")
    # bright.set_title('Total')


population = None
errors = []

def init():
    global population
    top.set_xscale('log')
    top.set_yscale('log')
    main.set_xscale('log')
    main.set_yscale('log')
    main.set_ylim(1e-3, 1e3)
    main.set_xlim(1e-14, 1e-2)
    top.set_ylim(5, 6)
    top.set_xlim(4e-5, 5e-5)
    bottom.set_xlim(0, 30)
    population = Population(100, discharge=8.155, radius=582, data_file="./data.csv")
    bottom.set_ylim(0, 2)

def update(i):
    global population, errors
    if (i % 5) == 0:
        gc.collect()

    x = [o.storativity for o in population.organisms]
    y = [o.transmissivity for o in population.organisms]
    errors.append([population.organisms[i].error for i in range(10)])

    for i in range(10):
        err_plts[i].set_data(range(len(errors)),[err[i] for err in errors])
    population_plt.set_offsets(np.c_[x,y])
    # population_plt.set_sizes([min([1, 100/(i+5)]) for _ in range(100)])
    zoom_plt.set_offsets(np.c_[x,y])

    population.next_generation()



anim = FuncAnimation(fig, update,
                     repeat=False,
                     blit=False,
                     frames=35,
                     cache_frame_data=False,
                     save_count=1,
                     init_func=init)


writer = PillowWriter(fps=2)
anim.save("/tmp/anim.gif", writer=writer)
print("Animation saved in {}".format("/tmp/anim.gif"))

plt.show()

