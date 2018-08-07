from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection, PolyCollection

def candlestick2_ohlc(ax,opens,highs,lows,closes,width=4,colorup='k',colordown='r',alpha=0.75,shift=0):
    delta=width/2.
    barVerts = [((i - delta + shift, open),
                 (i - delta + shift, close),
                 (i + delta + shift, close),
                 (i + delta + shift, open))
                for i, open, close in zip(xrange(len(opens)), opens, closes)
                if open != -1 and close != -1]
    rangeSegments = [((i, low), (i, high))
                     for i, low, high in zip(xrange(len(lows)), lows, highs)
                     if low != -1]
    colorup = mcolors.to_rgba(colorup, alpha)
    colordown = mcolors.to_rgba(colordown, alpha)
    colord = {True: colorup, False: colordown}
    colors = [colord[open < close]
              for open, close in zip(opens, closes)
              if open != -1 and close != -1]
    useAA=0
    lw=0.5
    rangeCollection=LineCollection(rangeSegments,colors=colors,linewidths=lw,antialiaseds=useAA)
    barCollection=PolyCollection(barVerts,facecolors=colors,edgecolors=colors,antialiaseds=useAA,linewidths=lw)
    minx,maxx=0,len(rangeSegments)
    miny=min([low for low in lows if low != -1])
    maxy=max([high for high in highs if high != -1])
    corners=(minx,miny),(maxx,maxy)
    ax.update_datalim(corners)
    ax.autoscale_view()
    if shift==0:
        ax.add_collection(rangeCollection)
    ax.add_collection(barCollection)
    return rangeCollection, barCollection