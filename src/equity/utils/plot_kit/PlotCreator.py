import matplotlib.pyplot as plt
import os

import pandas as pd


class PlotFinanceGraphs:
    def __init__(self,drop_folder: str):
        '''

        Parameters
        ----------
        drop_folder
        '''
        self.drop_plot_folder=drop_folder




    def manyPlots(self,arg,l_values,ls_labes,figName,xAxisName=None,yAxisName=None,title=None,):
        '''

        Parameters
        ----------
        arg
        l_values
        ls_labes
        figName
        xAxisName
        yAxisName
        title

        Returns
        -------

        '''
        os.chdir(self.drop_plot_folder)
        for i in range(len(l_values)):
            plt.plot(arg, l_values[i], label=ls_labes[i])

        plt.xlabel(xAxisName)
        plt.ylabel(yAxisName)
        plt.title(title)
        plt.legend()
        plt.savefig(figName)

    def define_plots_configuration(self,combination=111):
        '''

        Parameters
        ----------
        combination

        Returns
        -------

        '''
        return plt.subplot(combination)

    def plotDataFrameObject(self,df_scenarios:pd.DataFrame,index,combination:int,file_name:str,x_axis_name=None,y_axis_name=None,title=None,legend=None):
        '''

        Parameters
        ----------
        df_scenarios
        index
        combination
        file_name
        x_axis_name
        y_axis_name
        title
        legend

        Returns
        -------

        '''

        ax=self.define_plots_configuration(combination)
        if title is not None:
            ax.set_title(title)
        if x_axis_name is not None:
            ax.set_xlabel(x_axis_name)
        if y_axis_name is not None:
            ax.set_xlabel(y_axis_name)
        if  not isinstance(df_scenarios,pd.DataFrame):

            df_result=pd.DataFrame(df_scenarios,index=index)
            ax.plot(df_result)
            plt.savefig(file_name+'.png')
        elif isinstance(df_scenarios,pd.DataFrame):
            ax.plot(df_scenarios)













    def plotSurface(self):
        pass


