main_page_style = '''
                background-color: #2d2d2d;
                color: #C0C0C0;
                '''

menu_style = """
            QMenuBar {
                background-color: #3A3A3A;
                color: #C0C0C0;
                padding: 2.5px 1px;
                font-size: 13px;
            }

            QMenuBar::item:selected {
                background-color: #A9A9A9;
                color: white;
                border-radius: 3px;
            }

            QMenu {
                background-color: #3A3A3A;
                color: #C0C0C0;
                border-radius: 1px;
                padding: 2px 3px;
                border: 0.5px solid black;
            }

            QMenu::item:selected {
                background-color: #A9A9A9;
                color: white;
                border-radius: 4px;
            }
            
            QMenu::item {
                padding: 5px 20px;
                font-size: 13px;
            }
            """

graphic_view_style = """
            QGraphicsView {
                background-color: #2D2D2D;
                border: 1px solid black
            }
            
            QScrollBar:vertical {
                background-color: transparent;
                width: 8px;
            }

            QScrollBar::handle:vertical {
                background-color: #606060;
                border-radius: 4px;
                min-height: 20px;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;     
            }
            
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                border: none;
                background: none;
            }
            
            QScrollBar:horizontal {
                background-color: transparent;
                height: 8px;
            }

            QScrollBar::handle:horizontal {
                background-color: #606060;
                border-radius: 4px;
                min-height: 20px;
            }
            
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                border: none;
                background: none;                 
            }
            """

context_menu_style = '''
                QMenu {
                    background-color: #3A3A3A;
                    color: #C0C0C0;
                    padding: 2px 3px;
                    border: 0.5px solid black;
                }
                
                QMenu::item {
                    padding: 5px 20px;
                }
                
                QMenu::item:selected {
                    background-color: #A9A9A9;
                    color: white;
                    border-radius: 4px;
                }
                '''

side_style = '''
                QWidget {
                    background-color: #2d2d2d;
                }
                '''

table_style = """
            QTableWidget {
                border: none;
                text-align: center;
            }
            
            QHeaderView::section {
                background-color: #1e1e1e;
                color: white;
            }
            
            QTableCornerButton::section {
                background-color: #1e1e1e;
                color: white;
            }
            
            QTableWidget::item:alternate {
                background-color: #333333;
                color: white;
            }
            
            QTableWidget::item {
                background-color: #2b2b2b;
                color: white;
            }
            QScrollBar:vertical {
                background-color: transparent;
                border: none;
                width: 8px;
            }

            QScrollBar::handle:vertical {
                background-color: #606060;
                border-radius: 4px;
                min-height: 20px;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;                 
            }
            
            QScrollBar:horizontal {
                background-color: transparent;
                height: 8px;
            }

            QScrollBar::handle:horizontal {
                background-color: #606060;
                border-radius: 4px;
                min-height: 20px;
            }
            
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                border: none;
                background: none;                 
            }
            """
