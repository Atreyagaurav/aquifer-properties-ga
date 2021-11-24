#!/usr/bin/env python
import gc
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import pandas as pd

from genetic_alg import Population
import utilities
import config

colors10_rev = list(mcolors.TABLEAU_COLORS)
allcolors_rev = ['black'] * (config.GA_POPULATION_SIZE-len(colors10_rev)) + colors10_rev
allsize_rev = np.array([.4] * (config.GA_POPULATION_SIZE-len(colors10_rev)) + [1]*len(colors10_rev))

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
    data = pd.read_csv("./data/observed-data.csv")

    data_plot = curve.scatter(data.time, data.drawdown)

    curve.set_xscale('log')
    curve.set_yscale('log')
    est_plts = list(reversed([curve.plot([],[],
                           linewidth=1.5,
                           color=colors10_rev[i],
                                         alpha=1)[0] for i in range(10)]))
    est_plt_labels = [f'org-{i}' for i in range(10)]
    curve.legend(est_plts, est_plt_labels, ncol=2, fontsize='small')

    imgplot = main.pcolormesh(s_poss,t_poss,e, cmap='gist_rainbow', shading='auto', alpha=0.5)
    cb1 = plt.colorbar(imgplot, ax=main)
    imgplot2 = top.pcolormesh(s_poss2,t_poss2,e2, cmap='gist_rainbow', shading='auto', alpha=0.5)
    cb2 = plt.colorbar(imgplot2, ax=top)
    # imgplot.set_cmap('nipy_spectral')
    population_plt = main.scatter(range(config.GA_POPULATION_SIZE), range(config.GA_POPULATION_SIZE), c=allcolors_rev, s = allsize_rev*20)
    zoom_plt =        top.scatter(range(config.GA_POPULATION_SIZE), range(config.GA_POPULATION_SIZE), c=allcolors_rev, s = allsize_rev*20)
    err_plts = list(reversed([bottom.plot(range(config.GA_GENERATIONS),
                            range(config.GA_GENERATIONS),
                            linewidth=2,
                            alpha=1,
                            color=colors10_rev[i])[0]
                for i in range(10)]))
    err_plt_labels = [f'err-{i}' for i in range(10)]
    bottom.legend(err_plts, err_plt_labels, fontsize='small')

    fig.suptitle("Visualization of Genetic Algorithm in Curve Fitting")
    main.set_title("Original Sample Range")
    main.set_xlabel("Storativity →")
    main.set_ylabel("Transmissivity →")
    top.set_title("Solution Range")
    top.set_xlabel("Storativity →")
    top.set_ylabel("Transmissivity →")
    curve.set_xlabel("Time →")
    curve.set_ylabel("Drawdown →")
    bottom.set_title("Mean Absolute Error")


population = None
errors = []
best_model = None

def init():
    global population, best_model
    top.set_xscale('log')
    top.set_yscale('log')
    main.set_xscale('log')
    main.set_yscale('log')
    main.set_ylim(1e-1, 1e3)
    main.set_xlim(1e-14, 1e-2)
    top.set_ylim(5, 6)
    top.set_xlim(4e-5, 5e-5)
    bottom.set_xlim(0, config.GA_GENERATIONS)
    population = Population()
    bottom.set_ylim(0, 0.25)
    best_model = population.organisms[0]

def update(frame):
    global population, errors, best_model
    if population.organisms[0].error < best_model.error:
        best_model = population.organisms[0]
    
    if (frame % 5) == 0:
        gc.collect()
    x = [population.organisms[population.size-1- i].storativity for i in range(population.size)]
    y = [population.organisms[population.size-1- i].transmissivity for i in range(population.size)]
    errors.append([population.organisms[i].error for i in range(10)])

    for i in range(10):
        err_plts[i].set_data(range(len(errors)),[err[i] for err in errors])
        err_plt_labels[i] = f'${utilities.sci_2_latex(population.organisms[i].error)}$'
        est_plt_labels[i] = f'$S={utilities.sci_2_latex(population.organisms[i].storativity)}$' + \
            f',$T={utilities.sci_2_latex(population.organisms[i].transmissivity)}$'
        est_plts[i].set_data(data.time, population.organisms[i].estimated_drawdown)
    curve.legend(est_plts, est_plt_labels, ncol=2, fontsize='small', loc='lower right')
    bottom.legend(err_plts, err_plt_labels, ncol=2, fontsize='small')
    population_plt.set_offsets(np.c_[x,y])
    # population_plt.set_sizes([min([1, 100/(i+5)]) for _ in range(100)])
    zoom_plt.set_offsets(np.c_[x,y])

    print(f'Generation-{frame+1} :: error= {best_model.error} current best = {best_model}')
    fig.suptitle(f'Generation={frame+1:3d} Population={population.size} current best = {best_model}')
    population.next_generation()



anim = FuncAnimation(fig, update,
                     repeat=False,
                     blit=False,
                     frames=config.GA_GENERATIONS,
                     cache_frame_data=False,
                     save_count=1,
                     init_func=init)


writer = PillowWriter(fps=10)
anim.save("/tmp/anim.gif", writer=writer)
print("Animation saved in {}".format("/tmp/anim.gif"))

# plt.show()

