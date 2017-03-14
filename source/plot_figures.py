import matplotlib
matplotlib.use("TKAgg")
import numpy as np
import cPickle
from scipy.interpolate import interp1d
from numpy import linalg as LA
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import scipy.io as sio
import scipy.stats as sis
import os
import matplotlib.animation as animation
import math
import os.path


def adjustAxes(axes,axis_font,title_str, x_ticks, y_ticks):
    """Organize the axes of the given figure"""
    axes.set_xlim([0, 12.2])
    axes.set_ylim([0, 1.02])
    axes.set_title(title_str, fontsize=axis_font + 2)
    # axes[index].set_yticks(y_ticks)
    axes.tick_params(axis='y', labelsize=axis_font)
    axes.tick_params(axis='x', labelsize=axis_font)
    axes.set_xticks(x_ticks)
    axes.set_yticks(y_ticks)

def plot_all_epochs(I_XT_array, I_TY_array, axes, epochsInds, f, index_i, index_j, size_ind, font_size, y_ticks, x_ticks, colorbar_axis, title_str, axis_font, bar_font, save_name):
    """Plot the infomration plane with the epochs in diffrnet colors """
    max_index = size_ind if size_ind!=-1 else I_XT_array.shape[3]-1
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(i) for i in np.linspace(0, 1, epochsInds[max_index]+1)]
    #Change this if we have more then one network arch
    nums_arc= -1
    #The epoch that we want to emphasis in the figure
    index_to_emphasis = 10000
    #Go over all the epochs and plot then with the right color
    for index_in_range in range(max_index-1, max_index):
        XT, TY = [], []
        for layer_index in range(0, I_XT_array.shape[4]):
                XT.append(np.mean(I_XT_array[:, -1, nums_arc, index_in_range, layer_index], axis=0))
                TY.append(np.mean(I_TY_array[:, -1, nums_arc, index_in_range, layer_index], axis=0))
        if epochsInds[index_in_range] ==index_to_emphasis:
            axes[index_i, index_j].plot(XT, TY, marker='o', linestyle='-', markersize=19, markeredgewidth=0.04,
                                        linewidth=2.1,
                                        color='g',zorder=10)
        else:
            axes[index_i, index_j].plot(XT, TY, marker='o', linestyle='', markersize=12, markeredgewidth=0.01, linewidth=0.2,
                            color=colors[epochsInds[index_in_range]])
    #If we are in buttom sub-figure
    if index_i ==axes.shape[0]-1:
        axes[index_i, index_j].set_xlabel('$I(X;T)$', fontsize=font_size)
    #If we are in right sub-figure
    if index_j ==0:
        axes[index_i, index_j].set_ylabel('$I(T;Y)$', fontsize=font_size)
    #adjustAxes(axes[index_i, index_j], axis_font, title_str, x_ticks, y_ticks)
    #Save the figure and add color bar
    if index_i ==axes.shape[0]-1 and index_j ==axes.shape[1]-1:
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
        sm._A = []
        cbar_ax = f.add_axes(colorbar_axis)
        cbar = f.colorbar(sm, ticks=[], cax=cbar_ax)
        cbar.ax.tick_params(labelsize=bar_font)
        cbar.set_label('Epochs', size=bar_font)
        cbar.ax.text(0.5, -0.01, '0', transform=cbar.ax.transAxes,
                     va='top', ha='center', size=bar_font)
        cbar.ax.text(0.5, 1.0, '$10^4$', transform=cbar.ax.transAxes,
                     va='bottom', ha='center', size=bar_font)
        f.savefig(save_name+'.JPG', dpi=150, format='JPG')


def plot_by_training_samples(I_XT_array, I_TY_array, axes, epochsInds, f, index_i, index_j, size_ind, font_size, y_ticks, x_ticks, colorbar_axis, title_str, axis_font, bar_font, save_name):
    """Print the final epoch of all the diffrenet training samples size """
    max_index = size_ind if size_ind!=-1 else I_XT_array.shape[2]-1
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(i) for i in np.linspace(0, 1, max_index+1)]
    #Print the final epoch
    nums_epoch= -1
    #Go over all the samples size and plot them with the right color
    for index_in_range in range(0, max_index):
        XT, TY = [], []
        for layer_index in range(0, I_XT_array.shape[4]):
                XT.append(np.mean(I_XT_array[:, -1, index_in_range, nums_epoch, layer_index], axis=0))
                TY.append(np.mean(I_TY_array[:, -1, index_in_range,nums_epoch, layer_index], axis=0))
        axes[index_i, index_j].plot(XT, TY, marker='o', linestyle='-', markersize=12, markeredgewidth=0.2, linewidth=0.5,
                         color=colors[index_in_range])
    if index_i == axes.shape[0] - 1:
        axes[index_i, index_j].set_xlabel('$I(X;T)$', fontsize=font_size)
    adjustAxes(axes[index_i, index_j], axis_font, title_str, x_ticks, y_ticks)
    if index_j == 0:
        axes[index_i, index_j].set_ylabel('$I(T;Y)$', fontsize=font_size)
    #Create color bar and save it
    if index_i == axes.shape[0] - 1 and index_j == axes.shape[1] - 1:
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
        sm._A = []
        cbar_ax = f.add_axes(colorbar_axis)
        cbar = f.colorbar(sm, ticks=[], cax=cbar_ax)
        cbar.ax.tick_params(labelsize=bar_font)
        cbar.set_label('Training Data', size=bar_font)
        cbar.ax.text(0.5, -0.01, '3%', transform=cbar.ax.transAxes,
                     va='top', ha='center', size=bar_font)
        cbar.ax.text(0.5, 1.0, '85%', transform=cbar.ax.transAxes,
                     va='bottom', ha='center', size=bar_font)
        f.savefig(save_name + '.JPG', dpi=150, format='JPG')

def calc_velocity(data, epochs):
    """Calculate the velocity (both in X and Y) for each layer"""
    vXs, vYs = [], []
    for layer_index in range(data.shape[5]):
        curernt_vXs = []
        current_VYs = []
        for epoch_index in range(len(epochs)-1):
            vx = np.mean(data[0,:,-1, -1, epoch_index+1,layer_index], axis=0) - np.mean(data[0,:,-1, -1, epoch_index,layer_index], axis=0)
            vx/= (epochs[epoch_index+1] - epochs[epoch_index])
            vy = np.mean(data[1, :, -1, -1, epoch_index + 1, layer_index], axis=0) - np.mean(data[1, :, -1, -1, epoch_index, layer_index],                                                                      axis=0)
            vy /= (epochs[epoch_index + 1] - epochs[epoch_index])
            current_VYs.append(vy)
            curernt_vXs.append(vx)
        vXs.append(curernt_vXs)
        vYs.append(current_VYs)
    return vXs,vYs

def update_line_specipic_points(nums, data, axes, to_do, font_size, axis_font):
    """Update the lines in the axes for snapshot of the whole process"""
    colors = ['red', 'blue', 'green', 'yellow', 'pink', 'orange']
    x_ticks = [0, 2, 4, 6, 8, 10]
    #Go over all the snapshot
    for i in range(len(nums)):
        num = nums[i]
        #Plot the right layer
        for layer_num in range(data.shape[3]):
            axes[i].scatter(data[0, :, num, layer_num], data[1, :, num, layer_num], color = colors[layer_num], s = 105,edgecolors = 'black',alpha = 0.85)
        axes[i].set_xlim([0, 12.2])
        axes[i].set_ylim([0, 1.03])
        axes[i].set_xticks(x_ticks)
        axes[i].tick_params(axis='x', labelsize=axis_font)
        if to_do[i][0]:
            axes[i].set_xlabel('$I(X;T)$', fontsize=font_size)
            axes[i].tick_params(axis='x', labelsize=axis_font)
        if to_do[i][1]:
            axes[i].set_ylabel('$I(T;Y)$', fontsize=font_size)
            axes[i].tick_params(axis='y',labelsize=axis_font)

def update_line(num, print_loss, data, axes, epochsInds, train_data, test_data, epochs_bins, loss_train_data, loss_test_data, colors):
    """Update the figure of the infomration plane for the movie"""
    print num
    font_size = 18
    axis_font = 16
    #Print the line between the points
    cmap = ListedColormap(['red', 'green', 'blue', 'yellow', 'pink', 'orange'])
    segs = []
    for i in range(0, data.shape[1]):
        x = data[0, i, num, :]
        y = data[1, i, num, :]
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segs.append(np.concatenate([points[:-1], points[1:]], axis=1))
    segs = np.array(segs).reshape(-1, 2, 2)
    axes[0].clear()
    if len(axes)>1:
        axes[1].clear()
    lc = LineCollection(segs, cmap=cmap, linestyles='solid',linewidths = 0.3, alpha = 0.6)
    lc.set_array(np.arange(0,5))
    #Print the points
    for layer_num in range(data.shape[3]):
        axes[0].scatter(data[0, :, num, layer_num], data[1, :, num, layer_num], color = colors[layer_num], s = 35,edgecolors = 'black',alpha = 0.85)
    #the error
    axes[1].plot(epochsInds[:num], 1-np.mean(train_data[:,:num],axis=0),color = 'r')
    axes[0].set_xlim(0,12.2)
    axes[0].set_ylim(0.0, 1.08)
    axes[0].set_title('Information Plane - Epoch number - ' + str(epochsInds[num]), fontsize = axis_font)
    axes[0].set_ylabel('$I(T;Y)$', fontsize=font_size)
    axes[0].set_xlabel('$I(X;T)$', fontsize=font_size)
    axes[1].set_ylabel('Precision', fontsize=font_size)
    axes[1].set_xlabel('# Epochs', fontsize=font_size)
    axes[0].tick_params(axis='x', labelsize=axis_font)
    axes[0].tick_params(axis='y', labelsize=axis_font)
    axes[1].tick_params(axis='x', labelsize=axis_font)
    axes[1].tick_params(axis='y', labelsize=axis_font)
    axes[1].set_title('Precision as function of the epochs', fontsize = axis_font)

    #Print the loss function and the accuracy
    """"
    if len(axes)>1:
        axes[1].plot(epochsInds[:num], 1-np.mean(test_data[:,:num], axis=0), color='g')
        #axes[1].plot(epochsInds[:num], np.mean(loss_train_data[:, :num], axis=0), color='b')
        if print_loss:
            axes[1].plot(epochsInds[:num], np.mean(loss_test_data[:, :num], axis=0), color='y')
        nereast_val = np.searchsorted(epochs_bins, epochsInds[num], side='right')
        axes[1].set_xlim([0,epochs_bins[nereast_val]])
        axes[1].set_ylim([0, 0.9])
        axes[1].legend(('Accuracy', 'Loss Function'), loc='best')
    """

def load_reverese_annealing_data(name, max_beta = 300, min_beta=0.8, dt = 0.1):
    """Load mat file of the reverse annealing data with the give params"""
    with open(name + '.mat', 'rb') as handle:
        d = sio.loadmat(name + '.mat')
        F = d['F']
        ys = d['y']
        PXs = np.ones(len(F)) / len(F)
        f_PYs = np.mean(ys)
    PYs = np.array([f_PYs, 1 - f_PYs])
    PYX = np.concatenate((np.array(ys)[None, :], 1 - np.array(ys)[None, :]))
    mybetaS = 2 ** np.arange(np.log2(min_beta), np.log2(max_beta), dt)
    mybetaS = mybetaS[::-1]
    PTX0 = np.eye(PXs.shape[0])
    return mybetaS, np.squeeze(PTX0), np.squeeze(PXs), np.squeeze(PYX), np.squeeze(PYs)

def get_data(name):
    """Load data from the given name"""
    ws, loss_train_data, loss_test_data, information_each_neuron, norms1, norms2, gradients,epochs,train_data,test_data,loss_test_data =\
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    #new version
    if os.path.isfile(name + 'data.pickle'):
        curent_f = open(name + 'data.pickle', 'rb')
        d2 = cPickle.load(curent_f)
        epochs = d2['params']['epochsInds']
        I_XT_array2 = d2['information'][:, :, :, :, :, 0]
        I_TY_array2 = d2['information'][:, :, :, :, :, 1]
        data = np.array([I_XT_array2, I_TY_array2])
        train_data = d2['train_error']
        test_data = d2['test_error']
        params = d2['params']
        if 'ws_all' in d2:
            ws = d2['ws_all']
        if 'information_each_neuron' in d2:
            information_each_neuron = d2['information_each_neuron']
        if 'loss_train' in d2 and 'loss_test' in d2 :
            loss_train_data =d2['loss_train']
            loss_test_data = d2['loss_test']
        if 'var_grad_val' in d2:
            gradients = d2['var_grad_val']
        if 'l1_norms' in d2 and 'l2_norms' in d2:
            norms1 = d2['l1_norms']
            norms2 = d2['l2_norms']
        epochsInds = (params['epochsInds']).astype(np.int)
        #epochsInds = np.arange(0, data.shape[4])
        normalization_factor = 1
    #Old version
    else:
        curent_f = open(name, 'rb')
        d2 = cPickle.load(curent_f)
        data1 = d2[0]
        data =  np.array([data1[:, :, :, :, :, 0], data1[:, :, :, :, :, 1]])
        params = d2[-1]
        #Convert log e to log2
        normalization_factor =1/np.log2(2.718281)
        epochsInds = np.arange(0, data.shape[4])
        #epochsInds = np.round(2 ** np.arange(np.log2(1), np.log2(10000), .01)).astype(np.int)
    return data,epochs,train_data,test_data,ws,params,epochsInds,normalization_factor,information_each_neuron,loss_train_data,loss_test_data, \
           norms1, norms2,gradients

def plot_animation(name_s, save_name):
    """Plot the movie for all the networks in the information plane"""
    # If we want to print the loss function also
    print_loss  = False
    #The bins that we extened the x axis of the accuracy each time
    epochs_bins = [0, 500, 1500, 3000, 6000, 10000, 20000]
    data, epochs, train_data, test_data, ws, params, epochsInds, normalize_factor, information_each_neuron, loss_train_data, loss_test_data, norms1, norms2, gradients = get_data(name_s)
    f, (axes) = plt.subplots(2, 1)
    f.subplots_adjust(left=0.14, bottom=0.1, right=.928, top=0.94, wspace=0.13, hspace=0.55)
    colors = ['red', 'green', 'blue', 'yellow', 'pink', 'orange', 'purple', 'olive', 'black']
    #new/old version
    if False:
        Ix = np.squeeze(data[0,:,-1,-1, :, :])
        Iy = np.squeeze(data[1,:,-1,-1, :, :])
    else:
        Ix = np.squeeze(data[0, :, -1, -1, :, :])[np.newaxis,:,:]
        Iy = np.squeeze(data[1, :, -1, -1, :, :])[np.newaxis,:,:]
    #Interploation of the samplings (because we don't cauclaute the infomration in each epoch)
    interp_data_x = interp1d(epochsInds,  Ix, axis=1)
    interp_data_y = interp1d(epochsInds,  Iy, axis=1)
    new_x = np.arange(0,epochsInds[-1])
    new_data  = np.array([interp_data_x(new_x), interp_data_y(new_x)])
    """"
    train_data = interp1d(epochsInds,  np.squeeze(train_data), axis=1)(new_x)
    test_data = interp1d(epochsInds,  np.squeeze(test_data), axis=1)(new_x)
    """
    if print_loss:
        loss_train_data =  interp1d(epochsInds,  np.squeeze(loss_train_data), axis=1)(new_x)
        loss_test_data=interp1d(epochsInds,  np.squeeze(loss_test_data), axis=1)(new_x)
    line_ani = animation.FuncAnimation(f, update_line, len(new_x), repeat=False,
                                       interval=1, blit=False, fargs=(print_loss, new_data, axes,new_x,train_data,test_data,epochs_bins, loss_train_data,loss_test_data, colors))
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=100)
    #Save the movie
    line_ani.save(save_name+'_movie.mp4',writer=writer,dpi=250)
    plt.show()

def plot_snapshots(name_s, save_name, i):
    """Plot 3 snapshots of the given network"""
    font_size = 36
    axis_font = 28
    fig_size = (14, 6)
    f, (axes) = plt.subplots(1, 3, sharey=True, figsize=fig_size)
    f.subplots_adjust(left=0.095, bottom=0.18, right=.99, top=0.97, wspace=0.03, hspace=0.03)
    #What are the timesteps that we want ot plot
    time_stemps = [13, 180, 963]
    #Adding axes labels
    to_do = [[True, True], [True, False], [True, False]]
    data, epochs, train_data, test_data, ws, params, epochsInds, normalize_factor, information_each_neuron, loss_train_data, loss_test_data, norms1, norms2, gradients = get_data(name_s)
    data = np.squeeze(data)
    update_line_specipic_points(time_stemps, data, axes, to_do, font_size, axis_font)
    f.savefig(save_name + '.jpg', dpi=200, format='jpg')

def load_figures(mode):
    """Creaet new figure based on the mode of it"""
    if mode == 0:
        font_size = 34
        axis_font = 28
        bar_font = 28
        fig_size = (14, 6.5)
        title_strs = [['', '']]
        f, (axes) = plt.subplots(1, 2, sharey=True, figsize=fig_size)
        sizes = [[-1, 1400]]
        colorbar_axis = [0.935, 0.14, 0.027, 0.75]
        axes = np.vstack(axes).T
        f.subplots_adjust(left=0.09, bottom=0.15, right=.928, top=0.94, wspace=0.03, hspace=0.04)
        # for 3 rows with 2 colmus
    if mode == 1:
        font_size = 34
        axis_font = 26
        bar_font = 28
        fig_size = (14, 19)
        xticks = [1, 3, 5, 7, 9, 11]
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
        title_strs = [['One hidden layer', 'Two hidden layers'], ['Three hidden layers', 'Four hidden layers'],
                      ['Five hidden layers', 'Six hidden layers']]
        f, (axes) = plt.subplots(3, 2, sharex=True, sharey=True, figsize=fig_size)
        f.subplots_adjust(left=0.09, bottom=0.08, right=.92, top=0.94, wspace=0.03, hspace=0.15)
        colorbar_axis = [0.93, 0.1, 0.035, 0.76]
        sizes = [[1010, 1010], [1017, 1020], [1700, 920]]
    # one figure
    if mode == 2 or mode ==6:
        axis_font = 28
        bar_font = 28
        fig_size = (14, 10)
        font_size = 34
        f, (axes) = plt.subplots(1, len(str_names), sharey=True, figsize=fig_size)
        if len(str_names) == 1:
            axes = np.vstack(np.array([axes]))
        f.subplots_adjust(left=0.084, bottom=0.12, right=.87, top=0.99, wspace=0.03, hspace=0.03)
        colorbar_axis = [0.905, 0.12, 0.03, 0.82]
        xticks = [1, 3, 5, 7, 9, 11]
        yticks = [0.3, 0.5, 0.7, 0.9]
        sizes = [[-1]]
        title_strs = [['', '']]
    # one figure with error bar
    if mode == 3:
        fig_size = (14, 10)
        font_size = 36
        axis_font = 28
        bar_font = 25
        title_strs = [['']]
        f, (axes) = plt.subplots(1, len(str_names), sharey=True, figsize=fig_size)
        if len(str_names) == 1:
            axes = np.vstack(np.array([axes]))
        f.subplots_adjust(left=0.097, bottom=0.12, right=.90, top=0.99, wspace=0.03, hspace=0.03)
        sizes = [[-1]]
        colorbar_axis = [0.933, 0.125, 0.03, 0.83]
        xticks = [0, 2, 4, 6, 8, 10, 12]
        yticks = [0.3, 0.4, 0.6, 0.8, 1]
        # two figures second
    if mode == 4:
        font_size = 27
        axis_font = 18
        bar_font = 23
        fig_size = (14, 6.5)
        title_strs = [['', '']]
        f, (axes) = plt.subplots(1, 2, figsize=fig_size)
        sizes = [[-1, -1]]
        colorbar_axis = [0.948, 0.08, 0.025, 0.81]
        axes = np.vstack(axes).T
        f.subplots_adjust(left=0.061, bottom=0.15, right=.933, top=0.94, wspace=0.17, hspace=0.04)
        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
        xticks = [1, 3, 5, 7, 9, 11]
    return font_size, axis_font, bar_font, colorbar_axis, sizes, yticks, xticks,title_strs, f, axes

def plot_figures(str_names, mode, save_name):
    """Plot the data in the given names with the given mode"""
    [font_size, axis_font, bar_font, colorbar_axis, sizes, yticks, xticks,title_strs, f, axes] = load_figures(mode)
    #Go over all the files
    for i in range(len(str_names)):
        for j in range(len(str_names[i])):
            name_s = str_names[i][j]
            #Load data for the given file
            data, epochs, train_data, test_data, ws, params, epochsInds, normalize_factor, information_each_neuron, loss_train_data, loss_test_data,norms1, norms2, gradients = get_data(name_s)
            #convert between log2 and log e
            I_XT_array = data[0, :, :, :, :, :] / normalize_factor
            I_TY_array = data[1, :, :, :, :, :] / normalize_factor
            #Plot it
            if mode ==3:
                plot_by_training_samples(I_XT_array, I_TY_array, axes, epochsInds, f, i, j, sizes[i][j], font_size, yticks, xticks, colorbar_axis, title_strs[i][j], axis_font, bar_font, save_name)
            elif mode ==6:
                plot_norms(axes, epochsInds,norms1 ,norms2)
            else:
                plot_all_epochs(I_XT_array, I_TY_array, axes, epochsInds, f, i, j, sizes[i][j], font_size, yticks, xticks,
                                colorbar_axis, title_strs[i][j], axis_font, bar_font, save_name)


def plot_norms(axes, epochsInds, norms1, norms2):
    """Plot the norm l1 and l2 of the given name"""
    axes.plot(epochsInds, np.mean(norms1[:,0,0,:], axis=0), color='g')
    axes.plot(epochsInds, np.mean(norms2[:,0,0,:], axis=0), color='b')
    axes.legend(('L1 norm', 'L2 norm'))
    axes.set_xlabel('Epochs')


def sampleStandardDeviation(x):
    """calculates the sample standard deviation"""
    sumv = 0.0
    for i in x:
         sumv += (i)**2
    return math.sqrt(sumv/(len(x)-1))


def pearson(x,y):
    """calculates the PCC"""
    scorex, scorey = [], []
    for i in x:
        scorex.append((i)/sampleStandardDeviation(x))
    for j in y:
        scorey.append((j)/sampleStandardDeviation(y))
    # multiplies both lists together into 1 list (hence zip) and sums the whole list
    return (sum([i*j for i,j in zip(scorex,scorey)]))/(len(x)-1)


def plot_pearson(name):
    """Plot the pearsin coeff of  the neurons for each layer"""
    data, epochs, train_data, test_data, ws, params, epochsInds, normalize_factor, information_each_neuron, \
        loss_train_data, loss_test_data, norms1, norms2, gradients = get_data(name)
    f = plt.figure(figsize=(12, 8))
    axes = f.add_subplot(111)
    #The number of neurons in each layer - need to change it to be auto
    sizes =[10,7, 5, 4,3,2 ]
    #The mean of pearson coeffs of all the layers
    pearson_mean =[]
    #Go over all the layers
    for layer in range(len(sizes)):
        inner_pearson_mean =[]
        #Go over all the weights in the layer
        for k in range(len(ws)):
            ws_current = np.squeeze(ws[k][0][0][-1])
            #Go over the neurons
            for neuron in range(len(ws_current[layer])):
                person_t = []
                #Go over the rest of the neurons
                for neuron_second in range(neuron+1, len(ws_current[layer])):
                    pearson_c, p_val =sis.pearsonr(ws_current[layer][neuron], ws_current[layer][neuron_second])
                    person_t.append(pearson_c)
            inner_pearson_mean.append(np.mean(person_t))
        pearson_mean.append(np.mean(inner_pearson_mean))
    #Plot the coeff
    axes.bar(np.arange(1,7), np.abs(np.array(pearson_mean))*np.sqrt(sizes), align='center')
    axes.set_xlabel('Layer')
    axes.set_ylabel('Abs(Pearson)*sqrt(N_i)')
    rects = axes.patches
    # Now make some labels
    labels = ["L%d (%d nuerons)" % (i,j) for i,j in zip(xrange(len(rects)), sizes)]
    plt.xticks(np.arange(1,7), labels)


def update_axes(axes, xlabel, ylabel, xlim, ylim, title, xscale, yscale, x_ticks, y_ticks, p_0, p_1):
    """adjust the axes to the ight scale/ticks and labels"""
    font_size = 30
    axis_font = 25
    legend_font = 16
    categories =6*['']
    labels = ['$10^{-5}$', '$10^{-4}$', '$10^{-3}$', '$10^{-2}$', '$10^{-1}$', '$10^0$', '$10^1$']
    #If we want grey line in the midle
    #axes.axvline(x=370, color='grey', linestyle=':', linewidth = 4)
    #The legents of the mean and the std
    leg1 = plt.legend([p_0[0],p_0[1],p_0[2],p_0[3],p_0[4], p_0[5]], categories, title=r'$\|Mean\left(\nabla{W_i}\right)\|$', loc='best',fontsize = legend_font,markerfirst = False, handlelength = 5)
    leg2 = plt.legend([p_1[0],p_1[1],p_1[2],p_1[3],p_1[4], p_1[5]], categories, title=r'$STD\left(\nabla{W_i}\right)$', loc='best',fontsize = legend_font ,markerfirst = False,handlelength = 5)
    leg1.get_title().set_fontsize('21')  # legend 'Title' fontsize
    leg2.get_title().set_fontsize('21')  # legend 'Title' fontsize
    plt.gca().add_artist(leg1)
    plt.gca().add_artist(leg2)
    axes.set_xscale(xscale)
    axes.set_yscale(yscale)
    axes.set_xlabel(xlabel,fontsize=font_size)
    axes.set_ylabel(ylabel, fontsize=font_size)
    axes.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axes.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axes.set_xticks(x_ticks)
    axes.set_yticks(y_ticks )
    axes.tick_params(axis='x', labelsize=axis_font)
    axes.tick_params(axis='y', labelsize=axis_font)
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    axes.xaxis.major.formatter._useMathText = True
    axes.set_yticklabels(labels)
    axes.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))


def update_axes_norms(axes, xlabel, ylabel):
    """Adjust the axes of the norms figure with labels/ticks"""
    font_size = 30
    axis_font = 25
    legend_font = 16
    #the legends
    categories = [r'$\|W_1\|$', r'$\|W_2\|$', r'$\|W_3\|$', r'$\|W_4\|$', r'$\|W_5\|$', r'$\|W_6\|$']
    #Grey line in the middle
    axes.axvline(x=370, color='grey', linestyle=':', linewidth=4)
    axes.legend(categories , loc='best', fontsize=legend_font)
    axes.set_xlabel(xlabel, fontsize=font_size)
    axes.set_ylabel(ylabel, fontsize=font_size)
    axes.tick_params(axis='x', labelsize=axis_font)
    axes.tick_params(axis='y', labelsize=axis_font)


def plot_gradients(name_s):
    """Plot the gradients and the means of the networks over the batchs"""
    data, epochs, train_data, test_data, ws, params, epochsInds, normalize_factor, information_each_neuron, loss_train_data, loss_test_data, norms1, norms2, gradients = get_data(
        name_s)
    traces_layers, means_layers,p_1, p_0 ,l2_norms= [],[], [], [],[]
    fig_size = (14, 10)
    f_norms, (axes_norms) = plt.subplots(1, 1, figsize=fig_size)
    f_log, (axes_log) = plt.subplots(1, 1,figsize=fig_size)
    f_log.subplots_adjust(left=0.097, bottom=0.11, right=.95, top=0.95, wspace=0.03, hspace=0.03)
    colors = ['red','c', 'blue', 'green', 'orange', 'purple']
    #TODO - change it to auto
    num_of_layer = 6
    #Go over the layers
    for layer_index in range(num_of_layer):
        #We want to skip the biasses so we need to go every 2 indexs
        layer = layer_index*2
        #Go over the wieghts
        for k in range(len(gradients)):
            grad = np.squeeze(gradients[k][0][0])
            ws_in = np.squeeze(ws[k][0][0])
            cov_traces ,means,means,layer_l2_norm= [], [] ,[],[]
            #Go over all the epochs
            for epoch_number in range(len(grad)):
                #the weights of the layer as one-dim vector
                if type(ws_in[epoch_number][layer_index]) is list:
                    flatted_list = [item for sublist in ws_in[epoch_number][layer_index] for item in sublist]
                else:
                    flatted_list = ws_in[epoch_number][layer_index]
                layer_l2_norm.append(LA.norm(np.array(flatted_list), ord=2))
                gradients_list = []
                #For each neuron go over all the weights
                for i in range(len(grad[epoch_number])):
                    current_list_inner = []
                    for neuron in range(len(grad[epoch_number][0][layer])):
                        c_n = grad[epoch_number][i][layer][neuron]
                        current_list_inner.extend(c_n)
                    gradients_list.append(current_list_inner)
                #the gradients are  dimensions of [#batchs][#weights]
                gradients_list = np.array(gradients_list)
                #the average over the batchs
                average_vec = np.mean(gradients_list, axis=0)
                #Sqrt of AA^T
                norm_mean = np.sqrt(np.dot(average_vec.T, average_vec))
                covs_mat = np.zeros((average_vec.shape[0], average_vec.shape[0]))
                #Go over all the vectors of batchs, reduce thier mean and calculate the covariance matrix
                for batch in range(gradients_list.shape[0]):
                    current_vec = gradients_list[batch, :] - average_vec
                    current_cov_mat = np.dot(current_vec[:,None], current_vec[None,:])
                    covs_mat+=current_cov_mat
                #Take the mean cov matrix
                mean_cov_mat = np.array(covs_mat)/ gradients_list.shape[0]
                #The trace of the cov matrix
                trac_cov = np.trace(mean_cov_mat)
                means.append(norm_mean)
                cov_traces.append(trac_cov)
                #Second method if we have a lot of neurons
                """
                #cov_traces.append(np.mean(grad_norms))
                #means.append(norm_mean)
                for neuron in range(len(grad[epoch_number][0][layer])/10):
                    gradients_list = np.array([grad[epoch_number][i][layer][neuron] for i in range(len(grad[epoch_number]))])
                    total_w.extend(gradients_list.T)
                    grad_norms1 = np.std(gradients_list, axis=0)
                    mean_la = np.abs(np.mean(np.array(gradients_list), axis=0))
                    #mean_la = LA.norm(gradients_list, axis=0)
                    c_var.append(np.mean(grad_norms1))
                    c_mean.append(np.mean(mean_la))
                #total_w is in size [num_of_total_weights, num of epochs]
                total_w = np.array(total_w)
                #c_var.append(np.sqrt(np.trace(np.cov(np.array(total_w).T)))/np.cov(np.array(total_w).T).shape[0])
                #print np.mean(c_mean).shape
                means.append(np.mean(c_mean))
                cov_traces.append(np.mean(c_var))
                """
            l2_norms.append(layer_l2_norm)
            means_layers.append(np.array(means))
            traces_layers.append((np.array(cov_traces)))
        #Normalize by the l_2 norms
        y_var = np.mean(np.array(traces_layers), axis=0)/np.mean(np.array(l2_norms), axis=0)
        y_mean = np.mean(np.array(means_layers), axis=0)/np.mean(np.array(l2_norms), axis=0)
        #Plot the gradients and the means
        c_p1, = axes_log.plot(epochsInds, y_var,markersize = 4, linewidth = 4,color = colors[layer_index], linestyle=':', markeredgewidth=0.2, dashes = [4,4])
        c_p0,= axes_log.plot(epochsInds, y_mean,  linewidth = 2,color = colors[layer_index])
        #plot the norms
        axes_norms.plot(epochsInds, np.mean(np.array(l2_norms), axis=0),linewidth = 2)
        #For the legend
        p_0.append(c_p0)
        p_1.append(c_p1)
    #adejust the figure according the specipic labels, scaling and legends
    #Change the log and log to linear if you want linear scaling
    update_axes(axes_log, '# Epochs', 'Normalized Mean and STD', [0, 7000], [0.000001, 10], '', 'log', 'log', [1, 10, 100, 1000, 7000], [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10], p_0, p_1)
    update_axes_norms(axes_norms, '# Epochs', '$L_2$')
    f_log.savefig('log_gradient.svg', dpi=200, format= 'svg')
    f_norms.savefig('norms.jpg', dpi=200, format= 'jpg')

if __name__ == '__main__':
    #The action the you want to plot
    #Plot snapshots of all the networks
    TIME_STEMPS = 'time-stemp'
    #create movie of the networks
    MOVIE = 'movie'
    #plot networks with diffrenet number of layers
    ALL_LAYERS = 'all_layers'
    #plot networks with 5% of the data and with 80%
    COMPRAED_PERCENT = 'compare_percent'
    #plot the infomration curves for the networks with diffrenet percent of the data
    ALL_SAMPLES = 'all_samples'
    #Choose whice figure to plot
    action = COMPRAED_PERCENT
    prex = 'jobsFiles/'
    sofix = '.pickle'
    prex2 = 'jobs/'
    #plot above action, the norms, the gradients and the pearson coeffs
    do_plot_action, do_plot_norms, do_plot_gradients, do_plot_pearson,  = True, False, False, False
    #str_names = [[prex2+'fo_layersSizes=[[10, 7, 5, 4, 3]]_LastEpochsInds=9998_numRepeats=1_batch=3563_DataName=reg_1_numEphocs=10000_learningRate=0.0004_numEpochsInds=964_samples=1_num_of_disribuation_samples=1/']]
    if action == TIME_STEMPS or action == MOVIE:
        index = 1
        name_s = prex2+ 'g_layersSizes=[[10, 7, 5, 4, 3]]_LastEpochsInds=9998_numRepeats=40_batch=3563_DataName=var_u_numEphocs=10000_learningRate=0.0002_numEpochsInds=964_samples=1_num_of_disribuation_samples=1/'
        name_s = prex2 +'r_DataName=MNIST_samples_len=1_layersSizes=[[400, 200, 150, 60, 50, 40, 30]]_learningRate=0.0002_numEpochsInds=677_numRepeats=1_LastEpochsInds=1399_num_of_disribuation_samples=1_numEphocs=1400_batch=2544/'
        if action ==TIME_STEMPS:
            save_name = '3_time_series'
            plot_snapshots(name_s, save_name, index)
        else:
            save_name  = 'genreal'
            plot_animation(name_s, save_name)
    else:
        if action ==ALL_LAYERS:
            mode =1
            save_name = ALL_LAYERS
            str_names = [[prex + 'ff3_5_198.pickle', prex+ 'ff3_4_198.pickle'],[prex + 'ff3_3_198.pickle',prex + 'ff3_2_198.pickle'],[prex + 'ff3_1_198.pickle',prex + 'ff4_1_10.pickle']]
            str_names[2][1] = prex2+'g_layersSizes=[[10, 7, 5, 4, 4, 3]]_LastEpochsInds=9998_numRepeats=20_batch=3563_DataName=var_u_numEphocs=10000_learningRate=0.0004_numEpochsInds=964_samples=1_num_of_disribuation_samples=1/'
        elif action == COMPRAED_PERCENT:
            save_name = COMPRAED_PERCENT
            mode =2
            str_names    = [[prex + 'ff4_1_10.pickle', prex + 'ff3_1_198.pickle']]
        elif action == ALL_SAMPLES:
            save_name = ALL_SAMPLES
            mode =3
            str_names = [[prex+'t_32_1.pickle']]
        str_names = [[prex2 +'r_DataName=MNIST_samples_len=1_layersSizes=[[400, 100, 50, 40, 30, 20]]_learningRate=0.0004_numEpochsInds=677_numRepeats=1_LastEpochsInds=1399_num_of_disribuation_samples=1_numEphocs=1400_batch=2544/']]
        if do_plot_action:
            plot_figures(str_names, mode, save_name)
        if do_plot_norms:
            plot_norms(str_names)
        if do_plot_pearson:
            plot_pearson(str_names)
        if do_plot_gradients:
            plot_gradients(str_names)
    plt.show()