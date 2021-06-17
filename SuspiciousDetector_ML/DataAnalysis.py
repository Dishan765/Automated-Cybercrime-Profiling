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

    def __init__(self, data_file_name,feature_col_name):
        self.df = pd.read_csv(data_file_name)
        self.feature_col_name = feature_col_name

    # for full dataset
    def generalInfo(self):
        total_comments = self.df[self.feature_col_name].count()
        print(f"Total No of Comments: {total_comments}")

        #Group data by source
        print("\tGROUP DATA BY SOURCE: ")
        source_type = self.df.groupby('Source', as_index=False).agg('count')
        print(source_type)
        print("***********************************************************************************************************")

        #No of suspicious and non-suspicious posts
        print("\tNO OF SUSPICIOUS AND NON-SUSPICIOUS POSTS: ")
        label_count = self.df.groupby(
            ['Labels'], as_index=True).agg(Count=('Source', 'count'))
        print(label_count)
        print("***********************************************************************************************************")

        # No of suspcious and non-suspicious post per source
        print("\tNO OF SUSPICIOUS AND NON-SUSPICIOUS POSTS PER SOURCE")
        label_type = self.df.groupby(
            ['Source', 'Labels'], as_index=True).Source.count()
        print(label_type)
        
    # Pie chart of % of comments from each source for full dataset
    def pie_chart(self):
        # Group data by source
        source_type = self.df.groupby('Source', as_index=False).agg('count')

        # Sort indices and counts for Source columns
        source_labels = source_type.Source
        source_counts = source_type.Comments

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


    # barchart of the labels for each source for full dataset
    def barchart_labels_per_source(self):
        # No of suspcious and non-suspicious post per source
        label_type = self.df.groupby(
            ['Source', 'Labels'], as_index=True).Source.count().unstack()
        
        # Plot the barchart
        label_type.plot(kind='bar', title="No of suspcious and non-suspicious posts per source").legend(
            loc='upper center', ncol=3)

        plt.figure(1, figsize=(40, 20))
        plt.show()
    
    
    def barchart_labels(self):
        count_classes = pd.value_counts(self.df['Labels'], sort = True)
        count_classes.plot(kind = 'bar', rot=0)
        plt.title("Labels Distribution") 
        plt.xlabel("Label")
        plt.ylabel("Frequency")
        plt.show()

    
    # # For trained data set only
    # def barchart_labels_train(self,df_train):
    #     target_count = df_train.target.value_counts()
    #     print('Class 0:', target_count[0])
    #     print('Class 1:', target_count[1])
    #     print('Proportion:', round(target_count[0] / target_count[1], 2), ': 1')

    #     target_count.plot(kind='bar', title='Count (target)');

    # def scatter_plot(self):
    #     zero = self.df[self.df['Labels']==0][0:50]
    #     one = self.df[self.df['Labels']==1][0:50]
    #     axes = zero.plot(kind='scatter',x='processed_comments',y='Labels',color='blue',label = 'zero')
    #     one = zero.plot(kind='scatter',x='processed_comments',y='Labels',color='red',label = 'one',ax = axes)
    #     plt.show()
        

if __name__ == '__main__':
    processed_dataset = "GenerateDataset/Datasets/processedDataset2.csv"
    analyse = DataAnalysis(processed_dataset, "processed_comments")

    analyse.generalInfo()
    analyse.pie_chart()
    analyse.barchart_labels()
    analyse.barchart_labels_per_source()