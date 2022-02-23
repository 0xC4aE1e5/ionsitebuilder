from tkinter import *
from tkinter import simpledialog
from base64 import b64encode
import webbrowser
import os
from tkinter.filedialog import *

root = Tk()
root.title("Ion Site Builder")

if os.name == "nt":
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
else:
    chrome_path = '/usr/bin/google-chrome %s'
html = """
<style>
    body {
        background-color: #fafafa;
        font-family: sans-serif;
    }
</style>
"""


class CustomText(Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result


def export():
    try:
        global html
        asksaveasfile(mode='w', defaultextension=".html").write(html)
    except Exception:
        pass


def importf():
    try:
        T.delete("1.0", END)
        T.insert("1.0", askopenfile(mode='r').read())
        update()
    except Exception:
        pass


def update():
    T.unbind("<<TextModified>>")
    T.delete("1.0", END)
    T.insert(END, html)
    T.bind("<<TextModified>>", updateFromText)


def updateFromText(_):
    global html
    T.unbind("<<TextModified>>")
    html = T.get("1.0", END)
    T.bind("<<TextModified>>", updateFromText)


def text(customTag="p", title="Text", text="Enter text:"):
    global html
    text = simpledialog.askstring(title, text)
    html += f"<{customTag}>" + text + f"</{customTag}>"
    update()


def textWithAttributes(customTag="p", attributes={}, title="Text", text="Enter text:", after=""):
    global html
    text = simpledialog.askstring(title, text)
    html += f"<{customTag}"
    for key, value in attributes.items():
        html += f" {key}='{value}'"
    html += ">" + text + f"</{customTag}>"
    html += after
    update()


def image():
    global html
    image = simpledialog.askstring(
        "Image", "Enter image url (for local, prepend file:/// and use slashes, not backslashes):")
    html += "<img src=" + image + "><br>"
    update()


Label(root, text="Ion Site Builder", font=("none", 20)).grid(
    row=0, column=0)
Label(root, text="Add a block:").grid(row=1, column=0)
Button(root, text="Header", command=lambda: text(
    customTag="h1", title="Header", text="Enter header text:")).grid(row=1, column=1)
Button(root, text="Text", command=text).grid(row=1, column=2)
Button(root, text="Image", command=image).grid(row=1, column=3)
Button(root, text="Link", command=lambda: textWithAttributes(customTag="a", attributes={"href": simpledialog.askstring(
    "Link", "Enter the Link URL:")}, title="Link", text="Enter the link text", after="<br>")).grid(row=1, column=4)
Button(root, text="Preview", command=lambda: webbrowser.get(chrome_path).open(
    f"data:text/html;base64,{b64encode(T.get('1.0', END).encode()).decode()}", new=2)).grid(row=1, column=5)

global T
T = CustomText(root, height=20, width=50)
T.grid(row=3, column=0, columnspan=6)
T.bind("<<TextModified>>", updateFromText)

Button(root, text="Import", command=importf).grid(
    row=4, column=0)
Button(root, text="Export", command=export).grid(row=4, column=1)

root.mainloop()
