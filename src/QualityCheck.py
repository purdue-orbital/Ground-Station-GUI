from tkinter import *


class QualityCheck:
    def __init__(self, place_window, check_name, column_place, row_place):
        self.ready = False

        self.quality_label = Label(place_window, text=check_name, font=('times', 12, 'underline'))
        self.quality_label.grid(row=row_place, column=column_place, sticky=S + E + W)

        self.quality_indicator = Label(bg="red", pady=5, padx=5)
        self.quality_indicator.grid(row=row_place + 1, column=column_place, sticky=N + S + E + W)

    def display_quality(self):
        if self.ready:
            self.quality_indicator.config(bg="green")
        else:
            self.quality_indicator.config(bg="red")


# Example Case
if __name__ == "__main__":
    example = Tk()
    example.title("Example of Quality Check")
    example.geometry("600x600")

    for column in range(10):
        example.columnconfigure(column, weight=1)

    for row in range(10):
        example.rowconfigure(row, weight=1)

    example_QDM_check = QualityCheck(example, "QDM", 0, 0)
    example_CDM_check = QualityCheck(example, "CDM", 1, 0)
    example_other_check = QualityCheck(example, "Other", 2, 0)
    example_other_check.quality_indicator.config(bg="green")

    example.mainloop()


