import matplotlib.pyplot as plt
from sklearn import tree
import graphviz

def tree_graph(tree_reg, plot_file, feature_names):
    fig = plt.figure(figsize=(14,5), facecolor="#e4f1fe")
    _ = tree.plot_tree(tree_reg, feature_names=feature_names, filled=True)
    plot_data = tree.export_graphviz(tree_reg, out_file=None, feature_names=feature_names, filled=True)
    graphviz.Source(plot_data, format="png")
    fig.savefig(plot_file)    

