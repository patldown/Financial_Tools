import os, time
import matplotlib.pyplot as plt
import matplotlib.dates as dates

def plot_lgraph(location, ctitle, cxlabel, cylabel, x, y, key, *args):
    
    ### Plots initial x & y
    leg_keys = []
    plt.plot(y)
    leg_keys.append(key)

    ### Adds overlays if included
    if 'args' in locals():
        x = 0
        while x < len(args):
            plt.plot(args[x+1])
            leg_keys.append(args[x+2])
            x += 3

    plt.title(ctitle)
    plt.xlabel(cxlabel)
    plt.ylabel(cylabel)
    plt.legend(leg_keys)

##    plt.text(0.95, 0.01, 'colored text in axes coords',
##        verticalalignment='bottom', horizontalalignment='right',
##        transform=ax.transAxes,
##        color='green', fontsize=15)
    
    plt.savefig(os.path.join(os.getcwd(), location, ctitle + '.png'))
    plt.pyplot.clf()
    plt.pyplot.close()
    

if __name__ == '__main__':
    plot_lgraph('technical_run_chart','CPU Usage', 'Time', 'Ram Usage', [0, 1, 2, 3, 4, 5],
                [0.22, 0.27, 0.4, 0.2, 0.34, 0.7], 'CPU1')
