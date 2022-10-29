import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pylab as plt

class IOTools:
    @staticmethod
    def save_dfs_to_excel(df_list:list,
                          sheet_name:str,
                          file_name:str,
                          spaces: int):
        """save_dfs_to_excel _summary_

        _extended_summary_

        Parameters
        ----------
        df_list : list
            a list of dataframes
        sheet_name : str
            the name of the sheet
        file_name : str
            the full name of Excelfile
        spaces : int
            the number of spaces between the data frames in the excel file
        """
        writer=pd.ExcelWriter(file_name,engine='xlsxwriter')
        row=0
        for dataframe in df_list:
            dataframe.to_excel(writer,sheet_name=sheet_name,startrow=row,startcol=0)
            row=row+dataframe.shape[0]+spaces+1
        writer.save()    

    @staticmethod
    def save_df_to_csv(df:pd.DataFrame,
                      file_name:str):
       

        df.to_csv(file_name)    

    @staticmethod
    def plotUsingMatplot(ts_df_list,
                        ts_labels_list,
                        n_col,
                        n_row,
                        fig_size=(16,8),
                        adjust={"left":0.1,"bottom":0.1,"right":0.9,"top":0.9,"wspace":0.4,"hspace":0.4}):
        """method plotUsingMatplot _summary_
        Description
        -----------

        the function takes a list of dataframes where every dataframe represents time series.  Then it plots the time series using grids with dimension equal to n_row*n_col

        Parameters
        ----------
        ts_df_list : _type_
            list inlcuding time series dataframe, everydataframe must have two columns at least one for date and one for data
        ts_labels_list : _type_
            a list inlcuding labels of the time series
        n_col : _type_
            the number of columns for the grid of plot
        n_row : _type_
            the number of rows for the grid of plot
        fig_size : tuple, optional
            the size of the figure, by default (20,80)
        adjust : dict, optional
            adjustments for the picture, by default {"left":0.1,"bottom":0.1,"right":0.9,"top":0.9,"wspace":0.4,"hspace":0.4}
        """
        # --------------------
        # Region: Input Check
        # --------------------
        if len(ts_df_list)!=len(ts_labels_list):
            raise Exception("the length of the labels must match the length of the time series!")
        for ts_df in ts_df_list:
            if not isinstance(ts_df,pd.DataFrame) or ts_df.shape[1]<2 :
                raise Exception("The time series' data frames must have at least two columns where the first column "
                                "represents the dates and the second one the data. Make sure dataframes also have at "
                                "least twocolumns")   
        if n_col*n_row<len(ts_df_list):
            raise Exception("The number of time series exceeds the available sub-plots i.e. n_col*n_row. Increase "
            " the number of rows or columns in the plot grid.")                        

        # --------------------
        # End Region: Input Check
        # --------------------

        # --------------------
        # Region: plot
        # --------------------
        register_matplotlib_converters()
        fig, axes=plt.subplots(nrows=n_row,
                                ncols=n_col,
                                figsize=fig_size)
        axes_iter=iter(axes.reshape(-1))
        labels_iter=iter(ts_labels_list)
        for ts_df in ts_df_list:
            if ts_df.size>0:
                axe=next(axes_iter)
                axe.plot(ts_df)
                axe.set_title(next(labels_iter))
        plt.subplots_adjust(left=adjust.get("left"),
                            bottom=adjust.get("bottom"),    
                            right=adjust.get("right"),
                            top=adjust.get("top"),
                            wspace=adjust.get("wspace"),
                            hspace=adjust.get("hspace"))
        return fig,axes                                                    
        # --------------------
        # End Region: plot
        # --------------------