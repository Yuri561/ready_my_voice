def intro_txt(message, textbox):
    textbox.delete("1.0", "end")
    textbox.insert("1.0", message)

def process_command(command, textbox):
    textbox.insert("end", f"\n\n[Command received] {command}")