import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from tkinter import StringVar
import os
import detect_file
import database_logic
import detect_url
import time


HEIGHT = 550
WIDTH = 720

root = tk.Tk()
root.title('Trusty Scanner')
root.resizable(False, False)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

backgroundImage=tk.PhotoImage(file='images_data/third.png')
backgroundLabel=tk.Label(root,image=backgroundImage)
backgroundLabel.place(relwidth=1, relheight=1)


## frame
frame_menu = tk.Frame(root, bg='#60ba74')
frame_menu.place(relx=0.1, rely=0.1, relheight=0.2, relwidth=0.8)
## second frame
#frame_results = tk.Frame(root, bg='#60ba74')
#frame_results.place(relx=0.1, rely=0.4, relheight=0.5, relwidth=0.8)

def run_progress(progressbar, database):
    progressbar['maximum'] = len(database)
    #print(len(database))
    for i in range(len(database) + 1):
        time.sleep(0.00000000000000000000000000001)
        progressbar['value'] = i
        progressbar.update()
    #progressbar['value'] = 0

def run_progress_website(progressbar):
    progressbar['maximum'] = 150
    for i in range(151):
        time.sleep(0.03)
        progressbar['value'] = i
        progressbar.update()

def start_progress(progressbar):
    progressbar.start()

def stop_progress(progressbar):
    progressbar.stop()

## Scan File stuff all widgets in search file page
def browse_action_page():
    ## create new frame
    frame_results_file = tk.Frame(root, bg='#60ba74')
    frame_results_file.place(relx=0.1, rely=0.4, relheight=0.5, relwidth=0.8)
    cwd = os.getcwd()
    ##getting database to calculate len for printing output
    database = database_logic.import_data_from_database('database/malware_file_samples.data')
    ## getting filname with path from selecting in browse a file mode
    filename = filedialog.askopenfilename(initialdir = cwd, title = 'Select a file')
    ## if file im outputing all stuff that i need, label, progressbar, label_result
    if filename:
        ## Label for progress bar
        progress_label = tk.Label(frame_results_file, bg='#60ba74', font=33)
        progress_label['text'] = 'Scanning in progress...'
        progress_label.place(relx=0.29, rely=0.07, relwidth=0.4, relheight=0.2)
        ## style for progressbar basically i need black color
        style = Style()
        style.configure("black.Horizontal.TProgressbar", foreground='black', background='black')
        ## creating progress bar
        progress_bar = Progressbar(frame_results_file, orient='horizontal', mode = 'determinate', style='black.Horizontal.TProgressbar')
        progress_bar.place(relx=0.15, rely=0.33, relwidth=0.7, relheight=0.2)
        # creating result label to print
        result_label = tk.Label(frame_results_file, bg='#60ba74', font=40)
        result_label['text'] = ''
        result_label.place(relx=0.24, rely=0.66, relwidth=0.5, relheight=0.2)
        ## run progress bar
        run_progress(progress_bar, database)
        ## progressbar works until len(database) so i decide to print when its finished
        if progress_bar['value'] == len(database):
            detect_logic = detect_file.threaded_logic(filename)
            progress_label['text'] = 'Scan Finished!'
            result_label['text'] = detect_logic
        return detect_logic
    else:
        pass

## scan website and all widgets from search website page
def scan_site_page():
    frame_results_website = tk.Frame(root, bg='#60ba74')
    frame_results_website.place(relx=0.1, rely=0.4, relheight=0.5, relwidth=0.8)
    enter_site_label = tk.Label(frame_results_website, bg='#60ba74', font=33)
    enter_site_label['text'] = 'Enter website: '
    enter_site_label.place(relx=0.03, rely=0.07, relwidth=0.4, relheight=0.2)

    entry_id = StringVar()
    website_entry = tk.Entry(frame_results_website, textvariable=entry_id, bg='#60ba74', font=15)
    website_entry.place(relx=0.42, rely=0.11, relwidth=0.5, relheight=0.13)

    def click_scan_button_return(event):
        result_label['text'] = ''
        input_site = entry_id.get()
        if len(input_site) < 5 or '.' not in input_site:
            scanning_label['text'] = 'Enter a valid website!'
        else:
            scanning_label['text'] = 'Scanning in progress...'
            style = Style()
            style.configure("black.Horizontal.TProgressbar", foreground='black', background='black')
            progress_bar = Progressbar(frame_results_website, orient='horizontal', mode = 'determinate', style='black.Horizontal.TProgressbar')
            progress_bar.place(relx=0.15, rely=0.43, relwidth=0.7, relheight=0.2)
            run_progress_website(progress_bar)
            if progress_bar['value'] == progress_bar['maximum']:
                prediction = detect_url.load_model_and_predict('model_data/model.pkl', 'model_data/vectorizer.pkl',  [input_site])
                scanning_label['text'] = 'Scan Finished!'
                if prediction[0] == 'good':
                    result_label['text'] = 'Trusty website.'
                else:
                    result_label['text'] = 'On your Risk!'

    def click_scan_button():
        result_label['text'] = ''
        input_site = entry_id.get()
        if len(input_site) < 5 or '.' not in input_site:
            scanning_label['text'] = 'Enter a valid website!'
        else:
            scanning_label['text'] = 'Scanning in progress...'
            style = Style()
            style.configure("black.Horizontal.TProgressbar", foreground='black', background='black')
            progress_bar = Progressbar(frame_results_website, orient='horizontal', mode = 'determinate', style='black.Horizontal.TProgressbar')
            progress_bar.place(relx=0.15, rely=0.43, relwidth=0.7, relheight=0.2)
            run_progress_website(progress_bar)
            if progress_bar['value'] == progress_bar['maximum']:
                prediction = detect_url.load_model_and_predict('model_data/model.pkl', 'model_data/vectorizer.pkl',  [input_site])
                scanning_label['text'] = 'Scan Finished!'
                if prediction[0] == 'good':
                    result_label['text'] = 'Trusty website.'
                else:
                    result_label['text'] = 'On your Risk!'


    scanning_label = tk.Label(frame_results_website, bg='#60ba74', font=5)
    scanning_label['text'] = ''
    scanning_label.place(relx=0.30, rely=0.25, relwidth=0.4, relheight=0.18)

    result_label = tk.Label(frame_results_website, bg='#60ba74', font=50)
    result_label['text'] = ''
    result_label.place(relx=0.40, rely=0.68, relwidth=0.2, relheight=0.1)

    scan_button = tk.Button(frame_results_website, text='Scan', bg='#101111', font=40, fg='#60ba74', activeforeground='#72ea9c', activebackground='#101111', command=click_scan_button)
    scan_button.place(relx = 0.40, rely = 0.81, relwidth=0.2, relheight=0.15)
    root.bind('<Return>', click_scan_button_return)

## all widgets in about page
def about_page():
    frame_results_website = tk.Frame(root, bg='#60ba74')
    frame_results_website.place(relx=0.1, rely=0.4, relheight=0.5, relwidth=0.8)
    file_database_text = tk.Label(frame_results_website, bg='#60ba74', font=50)
    file_database_text['text'] = 'Malicious File Database:'
    file_database_text.place(relx=0.11, rely=0.10, relwidth=0.4, relheight=0.18)

    file_database_value_label = tk.Label(frame_results_website, bg='#60ba74', font=50)
    data = database_logic.import_data_from_database('database/malware_file_samples.data')
    len_data = len(data)
    file_database_value_label['text'] = str(len_data)
    file_database_value_label.place(relx=0.60, rely=0.10, relwidth=0.2, relheight=0.18)

    website_database_text = tk.Label(frame_results_website, bg='#60ba74', font=50)
    website_database_text['text'] = 'Malicious Website Database:'
    website_database_text.place(relx=0.10, rely=0.35, relwidth=0.4, relheight=0.18)

    website_database_value_label = tk.Label(frame_results_website, bg='#60ba74', font=50)
    data_website = database_logic.import_data_from_database('database/malware_url_samples.data')
    len_data_website = len(data_website)
    website_database_value_label['text'] = str(len_data_website)
    website_database_value_label.place(relx=0.60, rely=0.35, relwidth=0.2, relheight=0.18)

    train_model_text_accuracy = tk.Label(frame_results_website, bg='#60ba74', font=50)
    train_model_text_accuracy['text'] = 'Train Model Accuracy:'
    train_model_text_accuracy.place(relx=0.145, rely=0.50, relwidth=0.4, relheight=0.18)

    train_model_value_label = tk.Label(frame_results_website, bg='#60ba74', font=50)
    train_model_value_label['text'] = '96 %'
    train_model_value_label.place(relx=0.60, rely=0.50, relwidth=0.2, relheight=0.18)

    pass

## file search stucff
file_button = tk.Button(frame_menu, text='Scan File',bg='#101111', font=40, fg='#60ba74', activeforeground='#72ea9c', activebackground='#101111', command=browse_action_page)
file_button.place(relx=0.02, rely=0.22, relwidth=0.3, relheight=0.5)

## url stuff
url_button = tk.Button(frame_menu, text='Scan Website', bg='#101111', font=40, fg='#60ba74', activeforeground='#72ea9c', activebackground='#101111', command=scan_site_page)
url_button.place(relx=0.35, rely=0.22, relwidth=0.3, relheight=0.5)

### about this app stuff
about_button = tk.Button(frame_menu, text='About APP', bg='#101111', font=40, fg='#60ba74', activeforeground='#72ea9c', activebackground='#101111', command=about_page)
about_button.place(relx=0.68, rely=0.22, relwidth=0.3, relheight=0.5)

root.mainloop()
