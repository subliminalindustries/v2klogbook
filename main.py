import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    logbook = {'voice_intensity': [],
               'tinnitus': [],
               'pain': [],
               'paraesthesia': [],
               'contraction': [],
               'taunt': [],
               'threat': [],
               'text': [],
               'datetime': []}

    with open('data/logbook.txt', 'r') as fp:
        line = fp.readline()
        date = None
        tinnitus = 0
        while line is not None:
            if line.startswith('date:'):
                date = line.replace('date:', '').replace('\n', '')
                line = fp.readline()
                tinnitus = 0
                continue

            s = line.split(' ', 1)
            if len(s) != 2:
                break

            time, line = s

            logbook['datetime'].append(f'{date} {time}')

            s = line.split(',', 1)
            if len(s) != 2:
                break

            voice_intensity, line = s

            voice_intensity = {'low': 1,
                               'medium': 2,
                               'high': 3,
                               'extreme': 4
                               }.get(voice_intensity)

            logbook['voice_intensity'].append(voice_intensity)
            logbook['pain'].append(str(line.find('pain') != -1))
            logbook['paraesthesia'].append(repr(line.find('paraesthesia') != -1))
            logbook['contraction'].append(repr(line.find('contraction') != -1))
            logbook['threat'].append(repr(line.find('threat') != -1))
            logbook['taunt'].append(repr(line.find('taunt') != -1))

            if line.find('tinnitus start') != -1:
                tinnitus = 1
            if line.find('tinnitus stop') != -1:
                tinnitus = 0
            if line.find('tinnitus increase') != -1:
                tinnitus += 1
            if line.find('tinnitus decrease') != -1:
                tinnitus -= 1

            logbook['tinnitus'].append(tinnitus)
            logbook['text'].append(line)

            line = fp.readline()

    def hover(event):
        try:
            xdata = event.xdata
            ydata = event.ydata
            x = int(np.round(xdata))
            y = int(np.round(ydata))

            for i, art in enumerate(artists):
                an = annotations[i]
                cont, data = art.contains(event)
                if cont:
                    an.xy = (x, y)
                    an.set_text(logbook['text'][x])
                    an.set_visible(True)
                else:
                    an.set_text("")
                    an.set_visible(False)

            fig.canvas.draw_idle()
        except TypeError:
            pass

    artists = []
    annotations = []
    colors = ['red', 'cyan', 'green', 'purple', 'magenta', 'teal', 'orange']

    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams['axes.ymargin'] = 0
    fig, axs = plt.subplots(7, 1, sharex='all')
    plt.subplots_adjust(wspace=.1, hspace=.6)

    for idx, k in enumerate(logbook.keys()):
        if k == 'datetime' or k == 'text':
            break

        ax = axs[idx]

        annot = ax.annotate('', xy=(0, 0), xytext=(5, 5), textcoords='offset points',
                            bbox=dict(boxstyle='round', fc='w'))
        annot.set_visible(False)
        annotations.append(annot)

        artist = ax.plot(logbook['datetime'], logbook[k], 'o-', label=k, color=colors[idx])
        artists.append(artist[0])

        ax.set_title(k)
        ax.set_xticks(ticks=logbook['datetime'], labels=logbook['datetime'], rotation=90)

    fig.canvas.mpl_connect('motion_notify_event', hover)
    plt.show()
