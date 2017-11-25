import pandas as pd
import numpy as np
from datetime import date
from numpy import loadtxt
import matplotlib.pyplot as plt
import csv
from tkinter import *
from math import *


def mortgage_Payoff_Table(Interest_Rate, Years, Payments_Year, Principal, Addl_Princ, start_date, per = None):

   
    pmt = np.pmt(rate=Interest_Rate/Payments_Year, nper=Years*Payments_Year, pv=Principal)
    #print (pmt)
    
    
    #ipmt = np.ipmt(Interest_Rate/Payments_Year, per, Years*Payments_Year, Principal)
    #ppmt = np.ppmt(Interest_Rate/Payments_Year, per, Years*Payments_Year, Principal)
    #print(ipmt, ppmt)
    
    rng = pd.date_range(start_date, periods=Years * Payments_Year, freq='MS')
    rng.name = "Payment_Date"
    
    df = pd.DataFrame(index=rng,columns=['Payment', 'Principal', 'Interest', 'Addl_Principal'], dtype='float')
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name = "Period"
    
    df["Payment"] = np.pmt(Interest_Rate/Payments_Year, Years*Payments_Year, Principal)
    
    df["Principal"] = np.ppmt(Interest_Rate/Payments_Year, df.index, Years*Payments_Year, Principal)
    df["Interest"] = np.ipmt(Interest_Rate/Payments_Year, df.index, Years*Payments_Year, Principal)
    df["Addl_Principal"] = Addl_Princ
    df["Cumulative_Principal"] = (df["Principal"] + df["Addl_Principal"]).cumsum().clip(lower = -Principal)
    df['Curr_Balance'] = Principal + df["Cumulative_Principal"]
    df = df.round(2)
    
    try:
        last_payment = df.query("Curr_Balance <= 0")["Curr_Balance"].idxmax(axis=1, skipna=True)
    except ValueError:
        last_payment = df.last_valid_index()
    
    df.ix[last_payment,'Principal'] = -df.ix[last_payment-1,'Curr_Balance']
    
    df = df.ix[0:last_payment]
    
    df.ix[last_payment, "Principal"] = -(df.ix[last_payment-1, "Curr_Balance"])
    df.ix[last_payment,'Payment'] = df.ix[last_payment, ['Principal', 'Interest']].sum()
    df.ix[last_payment, "Addl_Principal"] = 0
    
    payoff_date = df["Payment_Date"].iloc[-1]
    stats = pd.Series([payoff_date, Interest_Rate, Years, Principal, pmt, Addl_Princ, df["Interest"].sum()],index=["Payoff Date", "Interest Rate", "Years", "Principal", "Payment", "Additional Payment", "Total Interest"], )
    return df, stats


hidden = False 
def toggle_entry():
    global hidden
    if not hidden:
        e.grid()
    else:
        e.grid_forget()
    hidden = not hidden


def run_pre_set():
    input_configuration=[]
    with open('configuration.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        col = False
        for row in csvReader:
            if col == True:
                input_configuration.append(row)
            col = True
            
    
    data = []        
    for row in input_configuration:
        index = int(row[0])
        Interest_Rate = float(row[1])
        Years = float(row[2])
        Payments_Year = float(row[3])
        Principal = float(row[4])
        Addl_Princ = float(row[5])
        start_year = int(row[6])
        start_month = int(row[7])
        start_day = int(row[8])
        start_date = date(start_year, start_month, start_day)
    
    
        data.append(mortgage_Payoff_Table(Interest_Rate, Years, Payments_Year, Principal, Addl_Princ, start_date))
        
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, 1)
    for i in range(len(data)):
        data[i][0].plot(x='Payment_Date', y='Curr_Balance', label="Scenario 1", ax=ax)
        plt.title("Pay Off Timelines ");
    
    
    data2 = []
    labels = []
    for i in range(len(data)):
        y = data[i][0].set_index('Payment_Date')['Interest'].resample("A").sum().reset_index()
        y["Year"] = y["Payment_Date"].dt.year
        y.set_index('Year', inplace=True)
        y.drop('Payment_Date', 1, inplace=True)
        stats = data[i][1]
        label="%d years at %f with additional payment of %f"% (stats['Years'], stats['Interest Rate'], stats['Additional Payment'])
        data2.append(y)
        labels.append(label)
    
    y = pd.concat(data2, axis = 1)
    fig, ax = plt.subplots(1, 1)
    y.plot(kind="bar", ax=ax)
    
    plt.legend(labels, loc=1, prop={'size':10})
    plt.title("Interest Payments");
    
    
    plt.show()
    plt.close()
    
    
def run_custom(Interest_Rate_, Years_, Payments_Year_, Principal_, Addl_Princ_, start_date_):
    
    Interest_Rate = float(str(Interest_Rate_.get()))
    Years = int(str(Years_.get()))
    Payments_Year = int(str(Payments_Year_.get()))
    Principal = float(str(Principal_.get()))
    Addl_Princ = float(str(Addl_Princ_.get()))
    start_date_str = str(start_date_.get()).split("-")
    start_year = int(start_date_str[0])
    start_month = int(start_date_str[1])
    start_day = int(start_date_str[2])
    start_date = date(start_year, start_month, start_day)
    
    
    data = [mortgage_Payoff_Table(Interest_Rate, Years, Payments_Year, Principal, Addl_Princ, start_date)]
        
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, 1)
    for i in range(len(data)):
        data[i][0].plot(x='Payment_Date', y='Curr_Balance', label="Scenario 1", ax=ax)
        plt.title("Pay Off Timelines ");
    
    
    data2 = []
    labels = []
    for i in range(len(data)):
        y = data[i][0].set_index('Payment_Date')['Interest'].resample("A").sum().reset_index()
        y["Year"] = y["Payment_Date"].dt.year
        y.set_index('Year', inplace=True)
        y.drop('Payment_Date', 1, inplace=True)
        stats = data[i][1]
        label="%d years at %f with additional payment of %f"% (stats['Years'], stats['Interest Rate'], stats['Additional Payment'])
        data2.append(y)
        labels.append(label)
    
    y = pd.concat(data2, axis = 1)
    fig, ax = plt.subplots(1, 1)
    y.plot(kind="bar", ax=ax)
    
    plt.legend(labels, loc=1, prop={'size':10})
    plt.title("Interest Payments");
    
    
    plt.show()
    plt.close()

        
if __name__ == '__main__':
    
    root = Tk()
    
    
    '''Years = IntVar()
    Payments_Year = IntVar()
    Principal = DoubleVar()
    Addl_Princ = DoubleVar()
    start_date = IntVar()'''
    
    Label(root, text="Load From Pre-set Configuration?").grid(row=0, column=0)
    
    Label(root, text="Nominal Annual Interest Rate:").grid(row=1, column=0)
    Interest_Rate_ = Entry(root)
    Interest_Rate_.grid(row=1, column=1)


    
    Label(root, text="Total Years:").grid(row=2, column=0)
    Years_ = Entry(root)
    Years_.grid(row=2, column=1)

    
    Label(root, text="Number of Payments per Year:").grid(row=3, column=0)
    Payments_Year_ = Entry(root)
    Payments_Year_.grid(row=3, column=1)

    
    Label(root, text="Principal:").grid(row=4, column=0)
    Principal_ = Entry(root)
    Principal_.grid(row=4, column=1)

    
    Label(root, text="Fixed Payment per period:").grid(row=5, column=0)
    Addl_Princ_ = Entry(root)
    Addl_Princ_.grid(row=5, column=1)

    
    Label(root, text="Starting Date [YYYY-MM-DD]:").grid(row=6, column=0)
    start_date_ = Entry(root)
    start_date_.grid(row=6, column=1)
    
    Button(root, text='Run Custom', command= lambda: run_custom(Interest_Rate_, Years_, Payments_Year_, Principal_, Addl_Princ_, start_date_)).grid(row=7, column=0)
    Button(root, text="Run Default", command=run_pre_set).grid(row=7, column=1)
    '''e = Entry(root)
    e.grid(row=0, column=1)
    Button(root, text='Toggle entry', command=toggle_entry).grid(row=0, column=0)
    '''

    e = Entry(root)

    res = Label(root).grid(row=4, column = 0)

        
    root.mainloop()

    