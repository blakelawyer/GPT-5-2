import tkinter as tk
import openai

openai.api_key = "INSERT API KEY"

root = tk.Tk()
root.title("HackAI-2021: Virtual Nurse Questionnaire")

root.geometry("600x400")

background_image = tk.PhotoImage(file=r"pic.png")
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

symptomString = tk.StringVar()
ageString = tk.StringVar()

symptom = ""
age = ""


def submit():
    global symptom
    global age

    symptom = symptomString.get()
    age = ageString.get()

    symptomString.set("")
    ageString.set("")
    root.destroy()


prompt = ""
result = ""
temp = .2


def medical_diagnosis():
    global prompt
    global result
    global temp
    prompt = "Here is what the medical community recommends to treat "
    result = "Medical Diagnosis"
    temp = .7
    button1.config(fg='blue')
    button2.config(fg='black')
    button3.config(fg='black')


def home_remedy():
    global prompt
    global result
    global temp
    prompt = "Here are some home remedies to treat "
    result = "Home Remedies"
    temp = .5
    button1.config(fg='black')
    button2.config(fg='blue')
    button3.config(fg='black')


def uncle_GPT():
    global prompt
    global result
    global temp
    result = "Uncle GPT's Advice"
    prompt = "Hey, calm down, I've been in the field for longer than you've been alive. Not legally, but why should you care? Let's do this like back in the old days. Here's you take care of "
    temp = .3
    button1.config(fg='black')
    button2.config(fg='black')
    button3.config(fg='blue')


symptomLabel = tk.Label(root, text='Enter your symptoms (separated by commas): ', font=('calibre', 10, 'bold'))
symptomEntry = tk.Entry(root, textvariable=symptomString, font=('calibre', 10, 'normal'))

ageLabel = tk.Label(root, text='Enter your age:', font=('calibre', 10, 'bold'))
ageEntry = tk.Entry(root, textvariable=ageString, font=('calibre', 10, 'normal'))

confirmButton = tk.Button(root, text='Confirm', command=submit)

button1 = tk.Button(root, text="Medical Diagnosis", command=medical_diagnosis, fg='black')
button2 = tk.Button(root, text="Home Remedy", command=home_remedy, fg='black')
button3 = tk.Button(root, text="Uncle GPT's Advice", command=uncle_GPT, fg='black')

button1.grid(row=2, column=0)
button2.grid(row=2, column=1)
button3.grid(row=2, column=2)

symptomLabel.grid(row=0, column=0)
symptomEntry.grid(row=0, column=1)
ageLabel.grid(row=1, column=0)
ageEntry.grid(row=1, column=1)
confirmButton.grid(row=3, column=1)

team = tk.Button(root, text='Team GPT-5(-2)', font=('calibre', 10, 'bold'))
team.grid(row=4, column=1, pady=275)

root.mainloop()

text = "Symptoms:" + str(symptom) + ", Age:" + str(age) + ". What medical conditions might I have?"

response = openai.Answer.create(
    search_model="ada",
    model="curie",
    question=text,
    documents=[],
    examples_context="A diagnosis can be made with complete accuracy by telling a story.",
    examples=[["Symptoms: cough, fever, headache, fatigue, Age: 20. What medical conditions might I have?",
               "You may have: flu, cold, allergies"]],
    max_tokens=25,
    stop=["\n", "<|endoftext|>"],
    temperature=.8,
    n=1
)

answer = response["answers"][0]

# print("ANSWER: ", answer)  # debug

split_answer = answer.split(":")

try:
    all_diagnosis = split_answer[1].split(",")
except:
    all_diagnosis = split_answer[1]

diagnosis = []
for d in all_diagnosis:
    diagnosis.append(d)

# print("DIAGNOSIS: ", diagnosis) # debug

if result == "":
    result = "Medical Diagnosis"

root = tk.Tk()
root.title("HackAI-2021: Virtual Nurse Results")
root.geometry("900x600")
resultLabel = tk.Label(root, text=result, font=('calibre', 30, 'bold'))
resultText = tk.Text(root, height=800, width=550)
resultLabel.pack()
resultText.pack()

for d in diagnosis:

    # print("Current Diagnosis: ", d) # debug

    header = ""
    header += result + ":" + d

    if prompt == "":
        prompt == "Here is what the medical community recommends to treat "

    response = openai.Completion.create(
        engine="davinci",
        prompt=(prompt + d + ":"),
        temperature=temp,
        max_tokens=150,
        top_p=1,
        frequency_penalty=.8
    )


    # print(response["choices"][0]["text"]) # debug
    resultText.insert(tk.END, header + "\n" + response["choices"][0]["text"] + "\n\n")

root.mainloop()
