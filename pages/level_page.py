from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, 
    QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QToolBar,
    QStatusBar, QProgressBar, QGridLayout
)
from PyQt6.QtGui import QPixmap, QAction, QCursor
from PyQt6 import QtCore
from assets.styles.colors import Color
import json
from database import Database
from assets.tools import Tools

styles = "assets\styles\styles.css"
buttons = {1: {"title": "New lesson", "icon": r"assets\images\new_lesson_icon.jpg", "display": True}, 2: {"title": "Daily review", "icon": r"assets\images\daily_review_icon-removebg-preview.png", "display": True}, 3: {"title": "Translation quiz", "icon": r"assets\images\translation_icon-removebg-preview.png", "display": True}, 4: {"title": "Word match", "icon": r"assets\images\word_match_icon-removebg-preview.png", "display": True}, 5: {"title": "Word fill", "icon": r"assets\images\new_lesson_icon.jpg", "display": False}, 6: {"title": "Kanji spell", "icon": r"assets\images\kanji_spell_icon.png", "display": True}}
tools = Tools()

class ModeSelectButton(QWidget):
    def __init__(self, id):
        super().__init__()

        self.id = id

        self.button = QPushButton()

        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_label = QLabel(buttons[self.id]['title'])
        self.setFontSize(self.button_label, 22)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.button_label)
        self.button_layout.addStretch(1)
        self.button_icon = QLabel(self)
        pixmap = QPixmap(buttons[self.id]['icon']).scaled(40,40)
        print(buttons[self.id]['icon'])
        self.button_icon.setPixmap(pixmap)
        self.button_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.button_icon)
        self.button.setLayout(self.button_layout)

        self.button.setProperty("class", "levelButton")
        self.button.setProperty("id", str(self.id))
        self.button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button.clicked.connect(self.buttonClicked)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        with open(styles, 'r') as f:
            self.setStyleSheet(f.read())

    def buttonClicked(self):
        self.parent().buttonClicked(self.id)

    def setFontSize(self, obj: QWidget, size: int):
        font = obj.font()
        font.setPointSize(size)
        obj.setFont(font)

class LevelPage(QWidget):
    def __init__(self, level):
        super().__init__()
        self.user = 1

        self.level = level.upper()
        self.colors = Color()
        
        self.buttons = []
        self.progress_information = {"grammar": 0, "words": 0, "kanji": 0}
        self.total_information = {"grammar" : 0, "words": 0, "kanji": 0}
        print(self.level)

        self.db = Database()
        self.initProgressInformation()
        

        print(self.colors.get_level_color(self.level))

        self.outerContainer = QVBoxLayout()

        labelLayout = QHBoxLayout()
        labelLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1 = QLabel(self.level)
        self.setFontSize(label1, 60)
        label1.setStyleSheet(f"""
        color: #{self.colors.get_level_color(self.level)};
        font-family: Titillium;
       
        width: 300px;
        height: 100px;

        """)

        labelLayout.addWidget(label1)

        ## ------------------------- Progress bars

        self.progressBarContainer = QHBoxLayout()

        self.wordsProgressBar = QProgressBar()
        self.kanjiProgressBar = QProgressBar()
        self.grammarProgressBar = QProgressBar()
        
        self.wordsProgressBar.setMinimum(0)
        self.wordsProgressBar.setMaximum(self.total_information["words"])
        self.wordsProgressBar.setValue(self.progress_information["words"])
        self.wordsProgressBar.setTextVisible(False)

        self.wordsLabel = QLabel("Words learnt", self)
        self.setFontSize(self.wordsLabel, 14)
        self.wordsLearnCounter = QLabel(f'{self.progress_information["words"]}/{self.total_information["words"]}')
        self.setFontSize(self.wordsLearnCounter, 14)

        self.wordsProgressBarSubContainer = QHBoxLayout()

        dudWordsContainer1 = QHBoxLayout()
        dudWordsContainer1.addWidget(self.wordsLabel)
        dudWordsContainer1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dudWordsContainer2 = QHBoxLayout()
        dudWordsContainer2.addWidget(self.wordsLearnCounter)
        dudWordsContainer2.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.wordsProgressBarSubContainer.addLayout(dudWordsContainer1)
        self.wordsProgressBarSubContainer.addLayout(dudWordsContainer2)
        self.wordsProgressBarContainer = QVBoxLayout()
        self.wordsProgressBarContainer.addLayout(self.wordsProgressBarSubContainer)
        self.wordsProgressBarContainer.addWidget(self.wordsProgressBar)
        self.wordsProgressBarContainer.setContentsMargins(0,30,0,60)

        self.kanjiProgressBar.setMinimum(0)
        self.kanjiProgressBar.setMaximum(self.total_information["kanji"])
        self.kanjiProgressBar.setValue(self.progress_information["kanji"])
        self.kanjiProgressBar.setTextVisible(False)

        self.kanjiLabel = QLabel("Kanji learnt", self)
        self.setFontSize(self.kanjiLabel, 14)
        self.kanjiLearnCounter = QLabel(f'{self.progress_information["kanji"]}/{self.total_information["kanji"]}')
        self.setFontSize(self.kanjiLearnCounter, 14)

        self.kanjiProgressBarSubContainer = QHBoxLayout()

        dudKanjiContainer1 = QHBoxLayout()
        dudKanjiContainer1.addWidget(self.kanjiLabel)
        dudKanjiContainer1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dudKanjiContainer2 = QHBoxLayout()
        dudKanjiContainer2.addWidget(self.kanjiLearnCounter)
        dudKanjiContainer2.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.kanjiProgressBarSubContainer.addLayout(dudKanjiContainer1)
        self.kanjiProgressBarSubContainer.addLayout(dudKanjiContainer2)
        self.kanjiProgressBarContainer = QVBoxLayout()
        self.kanjiProgressBarContainer.addLayout(self.kanjiProgressBarSubContainer)
        self.kanjiProgressBarContainer.addWidget(self.kanjiProgressBar)
        self.kanjiProgressBarContainer.setContentsMargins(0,30,0,60)

        self.grammarProgressBar.setMinimum(0)
        self.grammarProgressBar.setMaximum(self.total_information["grammar"])
        self.grammarProgressBar.setValue(self.progress_information["grammar"])
        self.grammarProgressBar.setTextVisible(False)

        self.grammarLabel = QLabel("Grammar learnt", self)
        self.setFontSize(self.grammarLabel, 14)
        self.grammarLearnCounter = QLabel(f'{self.progress_information["grammar"]}/{self.total_information["grammar"]}')
        self.setFontSize(self.grammarLearnCounter, 14)

        self.grammarProgressBarSubContainer = QHBoxLayout()

        dudGrammarContainer1 = QHBoxLayout()
        dudGrammarContainer1.addWidget(self.grammarLabel)
        dudGrammarContainer1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dudGrammarContainer2 = QHBoxLayout()
        dudGrammarContainer2.addWidget(self.grammarLearnCounter)
        dudGrammarContainer2.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.grammarProgressBarSubContainer.addLayout(dudGrammarContainer1)
        self.grammarProgressBarSubContainer.addLayout(dudGrammarContainer2)
        self.grammarProgressBarContainer = QVBoxLayout()


        self.grammarProgressBarContainer.addLayout(self.grammarProgressBarSubContainer)
        self.grammarProgressBarContainer.addWidget(self.grammarProgressBar)
        self.grammarProgressBarContainer.setContentsMargins(0,30,0,60)

        self.progressBarContainer.addLayout(self.wordsProgressBarContainer)
        self.progressBarContainer.addLayout(self.kanjiProgressBarContainer)
        self.progressBarContainer.addLayout(self.grammarProgressBarContainer)

        ## ----------------------------- Buttons

        self.buttonLayout = QGridLayout()
        self.buttonLayout.setProperty("class", "buttonLayout")
        self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for b in range(len(list(buttons.keys()))):
            idx = list(buttons.keys())[b]
            if buttons[idx]['display']:
                self.buttons.append(ModeSelectButton(idx))
            
        self.buttonLayout.addWidget(self.buttons[0], 0, 2, 1, 3)
        self.buttonLayout.addWidget(self.buttons[1], 2, 0, 1, 3)
        self.buttonLayout.addWidget(self.buttons[2], 2, 4, 1, 3)
        self.buttonLayout.addWidget(self.buttons[3], 4, 0, 1, 3)
        self.buttonLayout.addWidget(self.buttons[4], 4, 4, 1, 3)

        self.outerContainer.addLayout(labelLayout)
        self.outerContainer.addLayout(self.progressBarContainer)
        self.outerContainer.addLayout(self.buttonLayout)

        self.outerContainer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        with open(styles, "r") as f:
            self.setStyleSheet(f.read())

        dudContainer = QHBoxLayout()
        dudContainer.setContentsMargins(90,50,90,50)
        dudContainer.addLayout(self.outerContainer)

        self.setLayout(dudContainer)

        self.updateProgressBars()

    def initProgressInformation(self):
        self.num_grammars = self.db.get_num_grammars_at_level(self.level)
        self.num_words = self.db.get_num_words_at_level(self.level)
        self.num_kanjis = self.db.get_num_kanjis_at_level(self.level)
        print(self.num_words)
        if self.num_grammars is not None and self.num_words is not None and self.num_kanjis is not None:
            if self.num_grammars == 0:
                self.total_information["grammar"] = 1
            else:
                self.total_information["grammar"] = self.num_grammars

            if self.num_words == 0:
                self.total_information["words"] = 1
            else:
                self.total_information["words"] = self.num_words

            if self.num_kanjis == 0:
                self.total_information["kanji"] = 1
            else:
                self.total_information["kanji"] = self.num_kanjis
 
        
        self.grammars_learnt = self.db.get_num_grammars_at_level_user(self.level, self.user)
        self.words_learnt = self.db.get_num_words_at_level_user(self.level, self.user)
        self.kanjis_learnt = self.db.get_num_kanjis_at_level_user(self.level, self.user)

        if self.grammars_learnt is not None and self.words_learnt is not None and self.kanjis_learnt is not None:
            self.progress_information["grammar"] = self.grammars_learnt
            self.progress_information["words"] = self.words_learnt
            self.progress_information["kanji"] = self.kanjis_learnt
            print(self.progress_information)

    def setFontSize(self, obj: QWidget, size: int):
        font = obj.font()
        font.setPointSize(size)
        obj.setFont(font)

    def buttonClicked(self, id):
        if id == 1:
            self.parent().displayNewLessonPage()
        elif id == 2:
            pass
        elif id == 3:
            pass
        elif id == 4:
            self.parent().displayWordMatchPage()
        elif id == 5:
            pass
        elif id == 6:
            self.parent().displayKanjiSpellPage()

    def updateProgressBars(self):
        self.grammarProgressBar.setValue(self.progress_information["grammar"])
        self.kanjiProgressBar.setValue(self.progress_information["kanji"])
        self.wordsProgressBar.setValue(self.progress_information["words"])
