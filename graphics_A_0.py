import os, time
import matplotlib.pyplot
import matplotlib.dates as dates

def plot_lgraph(location, ctitle, cxlabel, cylabel, x, y, key, *args):
    
    ### Plots initial x & y
    leg_keys = []
    matplotlib.pyplot.plot(y)
    leg_keys.append(key)

    ### Adds overlays if included
    if 'args' in locals():
        x = 0
        while x < len(args):
            matplotlib.pyplot.plot(args[x+1])
            leg_keys.append(args[x+2])
            x += 3

    matplotlib.pyplot.title(ctitle)
    matplotlib.pyplot.xlabel(cxlabel)
    matplotlib.pyplot.ylabel(cylabel)
    matplotlib.pyplot.legend(leg_keys)

    #if os.path.exists(os.path.join(os.getcwd(), '_'.join(ctitle.split('_')[1:]))) != True:
    #    os.mkdir(os.path.join(os.getcwd(), location, '_'.join(ctitle.split('_')[1:])))
    
    #matplotlib.pyplot.savefig(os.path.join(os.getcwd(), location, '_'.join(ctitle.split('_')[1:]), ctitle + '.png'))
    matplotlib.pyplot.savefig(os.path.join(os.getcwd(), location, ctitle + '.png'))
    matplotlib.pyplot.clf()
    matplotlib.pyplot.close()
    

if __name__ == '__main__':
    plot_lgraph('technical_run_chart','CPU Usage', 'Time', 'Ram Usage', [0, 1, 2, 3, 4, 5],
                [0.22, 0.27, 0.4, 0.2, 0.34, 0.7], 'CPU1')
