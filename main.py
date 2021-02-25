from tkinter import filedialog, messagebox, END, Frame, Label, Toplevel, Text, Button, Menu, WORD, Scrollbar, \
    Listbox, LabelFrame
from tkinter.tix import Tk
from nltk import word_tokenize
from pymorphy2 import MorphAnalyzer
from help import HELPTEXT
from about import ABOUTTEXT
import win32api
import pickle
import time

vocabulary = []


class Lexeme:
    def __init__(self, stem, part, ending):
        self.stem = stem
        self.part = part
        self.ending = ending

    def print_args(self):
        return self.stem, self.part, self.ending


def create_new_file():
    global vocabulary
    vocabulary = []
    outputText.delete(0, END)


def save_file():
    file_path = filedialog.asksaveasfilename()
    if file_path != "":
        f = open(file_path, 'wb')
        pickle.dump(outputText.get(0, END), f)
        f.close()


def open_file():
    global vocabulary
    file_path = filedialog.askopenfilename()
    if file_path != "":
        f = open(file_path, 'rb')
        words = pickle.load(f)
        for i in range(len(words)):
            outputText.insert(0, str(words[i]))
        f.close()


def print_open_file():
    file_path = filedialog.askopenfilename()
    print(file_path)
    if file_path:
        win32api.ShellExecute(0, 'print', file_path, None, '.', 0)


def clear_dictionary():
    global outputText
    if outputText:
        answer = messagebox.askyesno(
            title="Вопрос",
            message="Вы уверены, что хотите очистить словарь?")
        if answer:
            outputText.delete(0, END)


def add_word():
    global vocabulary
    start_time = time.time()
    words = {}
    analyzer = MorphAnalyzer()
    vocabulary.append(inputText.get(1.0, END))
    tokenize_sentence = word_tokenize(vocabulary[0])
    for word in tokenize_sentence:
        parse_word = analyzer.parse(word)[0]
        word_word = parse_word.word
        word_lemma = parse_word.normal_form
        word_tags = parse_word.tag.cyr_repr
        word_ending = list(set(word_word) - set(word_lemma))
        if word_word is not word_lemma:
            words.update({word_word: {'lemma': word_lemma, 'tag': word_tags, 'ending': word_ending}})
    sorted_words = sorted(words)
    for key in sorted_words:
        lexeme = Lexeme((words[key]['lemma']), (words[key]['tag']), (words[key]['ending']))
        outputText.insert(0, str(lexeme.stem) + '      ' + str(lexeme.part) + '      '
                          + str(lexeme.ending))
    end_time = time.time()
    result_time = end_time - start_time
    print(str(result_time) + " seconds")
    vocabulary.clear()


def help_menu():
    children = Toplevel()
    children.title('Help')
    children.geometry("660x340")
    outputHelpText = Text(children, height=20, width=80)
    scrollb = Scrollbar(children, command=outputHelpText.yview)
    scrollb.grid(row=4, column=8, sticky='nsew')
    outputHelpText.grid(row=4, column=0, sticky='nsew', columnspan=3)
    outputHelpText.configure(yscrollcommand=scrollb.set)
    outputHelpText.insert('end', HELPTEXT)
    outputHelpText.configure(state='disabled')


def about_program_menu():
    children = Toplevel()
    children.title('About program')
    children.title('Help')
    children.geometry("660x340")
    outputAboutText = Text(children, height=20, width=80)
    scrollb = Scrollbar(children, command=outputAboutText.yview)
    scrollb.grid(row=4, column=8, sticky='nsew')
    outputAboutText.grid(row=4, column=0, sticky='nsew', columnspan=3)
    outputAboutText.configure(yscrollcommand=scrollb.set)
    outputAboutText.insert('end', ABOUTTEXT)
    outputAboutText.configure(state='disabled')

def generate_form():
    global generated_form
    analyzer = MorphAnalyzer()
    lemma_text = lemmaText.get(1.0, END).replace('\n', "")
    lemma_for_generate = analyzer.parse(lemma_text)[0]
    tags_text = tagsText.get(1.0, END).replace('\n', "")
    s = tags_text
    tags_for_generate = s.replace(',', '').split()
    if lemma_text or tags_text:
        children = Toplevel()
        children.title('Generated word')
        children.geometry("300x150+300+300")
        started_temporary_generated_form = lemma_for_generate.inflect({tags_for_generate[0]})
        for i in range(len(tags_for_generate)):
            over_temporary_generated_form = started_temporary_generated_form.inflect({tags_for_generate[i]})
            generated_form = over_temporary_generated_form
        lemmaLabel = Label(children, text=generated_form.word)
        lemmaLabel.pack(padx=10, pady=30)
    else:
        messagebox.showerror(
            "Ошибка",
            "Заполните поля")


def generate_word():
    children = Toplevel()
    children.geometry("420x200+300+300")
    global lemmaText
    lemmaFrame = Frame(children, bd=10)
    lemmaLabel = Label(lemmaFrame, text='Лексема', width=7, height=2)
    lemmaLabel.pack(side='left')
    lemmaText = Text(lemmaFrame, height=1, width=20)
    lemmaText.pack(side='right')
    global tagsText
    tagsFrame = Frame(children, bd=10)
    tagsLabel = Label(tagsFrame, text='Тэги', width=7, height=2)
    tagsLabel.pack(side='left')
    tagsText = Text(tagsFrame, height=1, width=20)
    tagsText.pack(side='right')
    childrenFrame = Frame(children, bd=10)
    generateFormButton = Button(childrenFrame, text='Генерация слова', width=25, height=2)
    generateFormButton.config(command=generate_form)
    generateFormButton.pack(side='right')
    children.title('Генерация слова')
    lemmaFrame.pack(side='top')
    tagsFrame.pack(side='top')
    childrenFrame.pack(side='bottom')


class App(Tk):
    def __init__(self):
        super().__init__()
        # -----------------------------------------INPUT--------------------------------------------------
        global inputText
        inputFrame = LabelFrame(self, bd=5, text='Ввод текста')
        inputText = Text(inputFrame, height=10, width=95, wrap=WORD)
        # -------------------------------------------OUTPUT------------------------------------------------
        global outputText
        outputFrame = LabelFrame(self, bd=1, text='Вывод словаря')
        outputText = Listbox(outputFrame, height=10, width=125)
        scrollb = Scrollbar(outputFrame, command=outputText.yview)
        scrollb.grid(row=4, column=5, sticky='nsew')
        outputText.grid(row=4, column=0, sticky='nsew', columnspan=5)
        outputText.configure(yscrollcommand=scrollb.set)
        # ------------------------------------------MENU---------------------------------------------------
        mainMenu = Menu(self)
        fileSubMenu = Menu(mainMenu, tearoff=0)
        fileSubMenu.add_command(label="Новый файл", command=create_new_file)
        fileSubMenu.add_command(label="Открыть", command=open_file)
        fileSubMenu.add_command(label="Сохранить", command=save_file)
        fileSubMenu.add_command(label="Печать", command=print_open_file)
        fileSubMenu.add_command(label="Выход", command=self.exitFile)

        helpSubMenu = Menu(mainMenu, tearoff=0)
        helpSubMenu.add_command(label="Помощь", command=help_menu)
        helpSubMenu.add_command(label="О программе", command=about_program_menu)

        mainMenu.add_cascade(label="Файл", menu=fileSubMenu)
        mainMenu.add_cascade(label="Информация", menu=helpSubMenu)
        self.config(menu=mainMenu)
        # ------------------------------------------Buttons---------------------------------------------------
        buttonsFrame = Frame(self, bd=5)
        addWordsButton = Button(buttonsFrame, text='Добавить в словарь', width=25, height=2)
        addWordsButton.config(command=add_word)
        addWordsButton.pack(side='left')
        spaceLabel1 = Label(buttonsFrame, width=7, height=2)
        spaceLabel1.pack(side='left')
        addWordsButton = Button(buttonsFrame, text='Очистить словарь', width=25, height=2)
        addWordsButton.config(command=clear_dictionary)
        addWordsButton.pack(side='left')
        spaceLabel2 = Label(buttonsFrame, width=7, height=2)
        spaceLabel2.pack(side='left')
        generateNewWordsButton = Button(buttonsFrame, text='Сгенерировать слоформу', width=25, height=2)
        generateNewWordsButton.config(command=generate_word)
        generateNewWordsButton.pack(side='left')
        self.title('Автоматизированная система формирования словаря естественного языка')
        outputFrame.pack()
        inputFrame.pack()
        inputText.pack()
        buttonsFrame.pack()
        self.geometry('800x400')

    def exitFile(self):
        if outputText.get(0, END) != ():
            answer = messagebox.askyesno(
                title="Вопрос",
                message="Сохранить словарь?")
            if answer:
                save_file()
                self.destroy()
            else:
                self.destroy()
        else:
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
