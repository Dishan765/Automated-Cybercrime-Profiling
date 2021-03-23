import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import tkinter

#import re

# import numpy as np
# import nltk
# %matplotlib inline


class DataAnalysis():

    def __init__(self, data_file_name):
        self.df = pd.read_csv(data_file_name)

    # Pie chart of % of comments from each source
    def pie_chart(self):
        total_comments = self.df['Comments'].count()
        print(f"Total No of Comments: {total_comments}")

        # Group data by source
        source_type = self.df.groupby('Source', as_index=False).agg('count')
        #source_type = self.df.groupby(['Source'], as_index=False, sort=False).count()
        print(source_type)

        # Sort indices and counts for Source columns
        source_labels = source_type.Source
        source_counts = source_type.Comments
        # print(source_labels.to_numpy())
        # print(source_counts.to_numpy())

        # Figure Details
        plt.figure(1, figsize=(20, 10))
        the_grid = GridSpec(2, 2)

        # Colour map information
        cmap = plt.get_cmap('Spectral')
        colors = [cmap(i) for i in np.linspace(0, 1, 8)]

        # Plot the pie chart
        plt.subplot(the_grid[0, 1], aspect=1, title='Sources of Comments')
        plt.pie(source_counts, labels=source_labels,
                autopct='%1.1f%%', shadow=True, colors=colors)
        plt.show()

    # barchart of the labels for each source
    def label_barchart(self):
        # No of suspcious and non-suspicious post
        #label_count = self.df.groupby(['Labels'], as_index=True).agg('count')
        label_count = self.df.groupby(
            ['Labels'], as_index=True).agg(Count=('Source', 'count'))
        print(label_count)

        # label_count.plot(kind='bar')
        # plt.show()

        # No of suspcious and non-suspicious post per source
        label_type = self.df.groupby(
            ['Source', 'Labels'], as_index=True).Source.count().unstack()
        print(label_type)

        label_type.plot(kind='bar', title="No of suspcious and non-suspicious posts per source").legend(
            loc='upper center', ncol=3)
        plt.show()


def main():
    da = DataAnalysis("SmallDatasets/smallDataset.csv")
    #da = DataAnalysis("SmallDatasets/processSmallDataset.csv")
    # da.pie_chart()
    da.label_barchart()


if __name__ == "__main__":
    main()
