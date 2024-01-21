import matplotlib.pyplot as plt
from sklearn import tree
import graphviz

def tree_graph(tree_reg, plot_file, feature_names):
    fig = plt.figure(figsize=(14,5))
    plot_data = tree.export_graphviz(tree_reg, out_file=None, feature_names=feature_names, filled=True)
    graphviz.Source(plot_data, format="png")
    fig.savefig("plot.png")    

