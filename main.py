import matplotlib.pyplot as plt


def set_ax_size(w=None, h=None, ax=None):
    if not ax:
        ax = plt.gca()

    if not w:
        w = ax.figure.get_width()

    if not h:
        h = ax.figure.get_height()

    ax_l = ax.figure.subplotpars.left
    ax_r = ax.figure.subplotpars.right
    ax_t = ax.figure.subplotpars.top
    ax_b = ax.figure.subplotpars.bottom

    fig_w = float(w)/(ax_r-ax_l)
    fig_h = float(h)/(ax_t-ax_b)

    ax.figure.set_size_inches(fig_w, fig_h)


if __name__ == '__main__':
    logbook = {'datetime': [],
               'voice_intensity': [],
               'pain': [],
               'paraesthesia': [],
               'contraction': [],
               'taunt': [],
               'threat': [],
               'tinnitus': []}

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

            line = fp.readline()

    fig, axs = plt.subplots(7, 1, sharex='all')
    for idx, k in enumerate(logbook.keys()):
        if k == 'datetime':
            continue

        axs[idx - 1].plot(logbook['datetime'], logbook[k])
        axs[idx - 1].set_ylabel(k)
        axs[idx - 1].set_xticks(ticks=logbook['datetime'], labels=logbook['datetime'], rotation=90)

        # set_ax_size(h=20, ax=axs[idx - 1])

    plt.show()
