from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFrame


class ReferenceDialog(QDialog):
    '''
    Custom QDialog class allowing user to specify the edge weight.

    Attributes:
        - algo_name (String): Name of the algorithm to display info of.
        - references (dictionary): Contains the reference and reference link for each algorithm
    '''
    def __init__(self, algo_name):
        '''
        Initialize a new instance of ReferenceDialog
        '''
        super(ReferenceDialog, self).__init__()

        self.algo_name = algo_name
        self.references = {
            'Degree': ['', 'https://en.wikipedia.org/wiki/Degree_(graph_theory)'],
            'Betweenness': ['Brandes, U. (2008). On variants of shortest-path betweenness centrality and their generic computation. Social Networks, 30(2), 136-145.', 'https://www.sciencedirect.com/science/article/abs/pii/S0378873307000731'],
            'Edge Betweenness': ['Brandes, U. (2008). On variants of shortest-path betweenness centrality and their generic computation. Social Networks, 30(2), 136-145.', 'https://www.sciencedirect.com/science/article/abs/pii/S0378873307000731'],
            'Closeness': ['', 'https://en.wikipedia.org/wiki/Closeness_centrality'],
            'Spanning Edge Betweenness': ['Teixeira, A., S., Monteiro, P., T., Carrico, J., A., Ramirez, M., Francisco, A., P. (2013). Spanning edge betweenness. In Workshop on Mining and Learning with Graphs, 24:27-31.', 'https://www.researchgate.net/publication/284626789_Spanning_edge_betweenness'],
            'TreeC': ['Mavroforakis, C., Garcia-Lebron, R., Koutis, I., & Terzi, E. (2015). Spanning edge centrality: Large-scale computation and applications. In Proceedings of the 24th International Conference on World Wide Web (pp. 732–742).', 'https://www.cs.cmu.edu/~jkoutis/papers/spanning_edge.pdf'],
            'Fast-TreeC': ['Mavroforakis, C., Garcia-Lebron, R., Koutis, I., & Terzi, E. (2015). Spanning edge centrality: Large-scale computation and applications. In Proceedings of the 24th International Conference on World Wide Web (pp. 732–742).', 'https://www.cs.cmu.edu/~jkoutis/papers/spanning_edge.pdf'],
            'TGT': ['Zhang, S., Yang, R., Tang, J., Xiao, X., & Tang, B. (2023). Efficient approximation algorithms for spanning centrality. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (pp. 3386–3395).', 'https://dl.acm.org/doi/abs/10.1145/3580305.3599323']
        }
        self.setWindowTitle('References')
        self.setWindowIcon(QIcon('Icons\\logo.png'))
        self.initUI()

    def initUI(self):
        '''
        Initialize dialog window's UI
        '''
        layout = QVBoxLayout(self)

        # Title
        title = QLabel(self.algo_name)
        title.setStyleSheet('font-size: 13px;')
        layout.addWidget(title)

        # Empty line
        layout.addSpacing(10)

        # Graph properties section
        graph_label = QLabel("References")
        graph_label.setWordWrap(True)
        layout.addWidget(graph_label)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        reference_text = self.references[self.algo_name][0]
        if reference_text:
            reference = QLabel(reference_text)
            layout.addWidget(reference)
            layout.addSpacing(10)

        link_text = self.references[self.algo_name][1]
        link = QLabel(f'<a href="{link_text}">{link_text}</a>')
        link.setOpenExternalLinks(True)
        layout.addWidget(link)

        self.setLayout(layout)
