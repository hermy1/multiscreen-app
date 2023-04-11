from tkinter import *
import math



class MultiFrameApp(Tk):
    def __init__(self, screenName=None, baseName=None, className='Tk',
                 useTk=True, sync=False, use=None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry('800x600')
        container = Frame(self)
        container.pack(fill='both', expand=True, side='top')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        bmi = BMIWindow(container, self)
        bmi.grid(row=0, column=0, sticky='news')
        calc = CalculatorFrame(container, self)
        calc.grid(row=0, column=0, sticky='news')


        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='BMI', command=lambda: self.show_frame('bmi'))
        self.file_menu.add_command(label='Calculator', command=lambda: self.show_frame('calc'))
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)


        self.frames = {
            'bmi': bmi,
            'calc': calc,
        }
        self.show_frame('bmi')

    def show_frame(self, frame_name: str):
        frame = self.frames[frame_name]
        frame.tkraise()


class CalculatorFrame(Frame):
    def __init__(self, container:Frame,controller:MultiFrameApp):
        super().__init__(container)
        self.controller = controller
        for row in range(0, 6):
            self.rowconfigure(row, weight=1)
        for col in range(0, 4):
            self.columnconfigure(col, weight=1)

        key_vals = ['Sqrt', '1/x', '(', ')', 'CLR', '/', '*', '-', 7, 8, 9, '+', 4, 5, 6, 1, 2, 3, '=', 0, '.']
        no_grid = [(4, 3), (6, 1), (6, 3)]
        row_span_2 = [(3, 3), (5, 3)]
        col_span_2 = [(6, 0)]
        self.font = ('Comic Sans MS', 18)
        self.bg = 'blue'
        self.fg = 'white'
        self.config(bg=self.bg)
        self.expression_var = StringVar()
        self.expression_var.set('')
        self.expression_label = Label(self, textvariable=self.expression_var,
                                      font=('Comic Sans MS', 22), bg='white',
                                      fg='blue', anchor='e')
        self.expression_label.grid(row=0, column=0, sticky='news', padx=3, pady=3,
                                   ipadx=3, ipady=3, columnspan=4)
        i = 0
        for row in range(1, 7):
            for col in range(0, 4):
                if (row, col) not in no_grid:
                    b = Button(self, text=key_vals[i], fg=self.fg,
                               bg=self.bg, font=self.font,
                               command=lambda val=key_vals[i]: self.update_expression(val))
                    rowspan = 1
                    colspan = 1
                    if (row, col) in row_span_2:
                        rowspan = 2
                    if (row, col) in col_span_2:
                        colspan = 2
                    b.grid(row=row, column=col, sticky='news', padx=3,
                           pady=3, ipadx=3, ipady=3,
                           columnspan=colspan, rowspan=rowspan)
                    i += 1

    def update_expression(self, val):
        if self.expression_var.get() == 'NaN':
            self.expression_var.set('')
        if val == 'CLR':
            self.expression_var.set('')
        elif val == '1/x':
            try:
                answer = str(1 / (eval(self.expression_var.get())))
                self.expression_var.set(answer)
            except:
                self.expression_var.set('NaN')
        elif val == 'Sqrt':
            try:
                answer = str(math.sqrt(eval(self.expression_var.get())))
                self.expression_var.set(answer)
            except:
                self.expression_var.set('NaN')
        elif val == '=':
            try:
                answer = str(eval(self.expression_var.get()))
                self.expression_var.set(answer)
            except:
                self.expression_var.set('NaN')
        else:
            expr = self.expression_var.get()
            expr = f'{expr}{val}'


class BMIOutOfRangeException(Exception):
    pass


class BMI:
    def __init__(self, weight: float, height: float) -> None:
        super().__init__()
        self.weight = weight
        self.height = height

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float):
        if value <= 0:
            raise BMIOutOfRangeException("Weight must be > 0")
        self._weight = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float):
        if value <= 0:
            raise BMIOutOfRangeException("Height must be > 0")
        self._height = value

    @property
    def value(self) -> float:
        return (703 * self._weight) / (self._height ** 2)

    @property
    def category(self) -> str:
        value = self.value
        category = ""
        if value < 18.5:
            category = "Underweight"
        elif value < 25:
            category = "Normal Weight"
        elif value < 30:
            category = "Overweight"
        elif value < 33:
            category = "Obese"
        else:
            category = "Morbidly Obese"
        return category

    @classmethod
    def get_bmi_value(cls,weight:float,height:float):
        return (703 * weight) / (height ** 2)

    @classmethod
    def get_bmi_category(cls, bmi_value:float):
        category = ""
        if bmi_value < 18.5:
            category = "Underweight"
        elif bmi_value < 25:
            category = "Normal Weight"
        elif bmi_value < 30:
            category = "Overweight"
        elif bmi_value < 33:
            category = "Obese"
        else:
            category = "Morbidly Obese"
        return category

    def __str__(self) -> str:
        return f'BMI{{weight:{self._weight}, height: {self._height}' + \
               f', value: {self.value},category: {self.category} }}'

    def __repr__(self) -> str:
        return self.__str__()


class BMIWindow(Frame):
    def __init__(self,container:Frame, controller:MultiFrameApp, title: str = "BMI Calculator", bg: str = 'blue',
                 fg='white',
                 title_font: tuple = ('Arial', 24, 'bold'), font: tuple = ('Arial', 18),
                 button_bg: str = 'black') -> None:
        super().__init__(container)
        self.controller = controller
        self.config(bg=bg)
        self.title_label = Label(self, text=title)
        self.title_label.pack()
        self.weight_label = Label(self, text="Weight")
        self.weight_label.pack()
        self.weight_entry = Entry(self)
        self.weight_entry.pack()
        self.height_label = Label(self, text="height")
        self.height_label.pack()
        self.height_entry = Entry(self)
        self.height_entry.pack()
        self.calculate_button = Button(self, text="Calculate",
                                          command=self.calculate)
        self.calculate_button.pack()
        self.value_label = Label(self)
        self.value_label.pack()
        self.category_label = Label(self)
        self.category_label.pack()
        self.common_styled = [self.weight_label,self.weight_entry,
                              self.height_label,self.height_entry,
                              self.value_label,self.category_label]
        for widget in self.common_styled:
            widget.config(fg=fg,bg=bg,font=font)
        self.title_label.config(fg=fg,bg=bg,font=title_font)
        self.calculate_button.config(fg=fg,bg=button_bg,font=font)


    def calculate(self):
        try:
            weight = float(self.weight_entry.get())

            height = float(self.height_entry.get())
            '''bmi = BMI(weight, height)
            self.value_label.config(text=f'Value: {bmi.value:.2f}')
            self.category_label.config(text=f'Category: {bmi.category}')'''
            value = BMI.get_bmi_value(weight,height)
            category = BMI.get_bmi_category(value)
            self.value_label.config(text=f'Value: {value:.2f}')
            self.category_label.config(text=f'Category: {category}')
        except ValueError as ve:
            self.value_label.config(text='Value needs to be a number')
        except BMIOutOfRangeException as bmioore:
            self.value_label.config(text=str(bmioore))
        except Exception as ex:
            self._value_label.config(text=str(ex))


