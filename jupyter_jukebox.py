import ipywidgets as widgets
from IPython.display import display
from numpy import asarray
import matplotlib.pyplot as plt

# functions that are methods
__all__ = [
    'single_param_interact',
]

def single_param_interact(x,param_values,f,y_scale='stretch',slider_format_string='{:.1f}',plot_kwargs=None):
    """
    A function to easily create an interactive plot 1D with a slider for a parameter.
    
    parameters
    ----------
    x : arraylike
        x values a which to evaluate the function
    f : function
        Function with siganture f(x, param) where param is what you
        would like vary. Doesn't need to be named param
    param_values : arraylike
        The values of the parameter to be availiable in the slider
    y_scale : string or tuple of floats, optional
        If a tuple it will be passed to ax.set_ylim. Other options are:
        'auto': rescale the y axis for every redraw
        'stretch': only ever expand the ylims.
    slider_format_string : string
        A valid format string, this will be used to render
        the current value of the parameter
    plot_kwargs : None or dict
        Keyword arguments to pass to plot
    """
    x = asarray(x)
    param_values = asarray(param_values)
    
    if x.ndim != 1:
        raise ValueError(f'x must be 1D but is {x.ndim}')
    if param_values.ndim != 1:
        raise ValueError(f'param_values must be 1D but is {param_values.ndim}')
    if plot_kwargs is None:
        plot_kwargs = {}
    
    #create initial plot
    plt.ioff() # turn off interactive mode briefly to prevent extra figure appearing
    fig = plt.figure()
    ax = fig.gca()
    plt.ion()
    line = ax.plot(x,f(x,param_values[0]),**plot_kwargs)[0]
    if not isinstance(y_scale,str):
        ax.set_ylim(y_scale)
    
    # make widgets
    label = widgets.Label(value=f'{param_values[0]}')
    slider = widgets.IntSlider(min=0,max=param_values.size,readout=False)
    
    #update function
    def update(change):
        # update label
        label.value = slider_format_string.format(param_values[slider.value])
        
        # update plot
        line.set_data(x,f(x,param_values[slider.value]))
        cur_lims = ax.get_ylim()
        if y_scale=='auto':
            ax.relim()
            ax.autoscale_view()
            ax.set_
        elif y_scale=='stretch':
            ax.relim()
            new_lims = [ax.dataLim.y0, ax.dataLim.y0+ax.dataLim.height]
            new_lims = [
                new_lims[0] if new_lims[0]<cur_lims[0] else cur_lims[0],
                new_lims[1] if new_lims[1]>cur_lims[1] else cur_lims[1]
                ]
            ax.set_ylim(new_lims)
        fig.canvas.draw_idle()
    slider.observe(update,names='value')
    control = widgets.HBox([slider,label])
    
    display(widgets.VBox([control,fig.canvas]))
    return fig,ax