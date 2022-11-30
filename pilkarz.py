import os
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup
from requests import get
from tkinter import *

main_window = Tk()
main_window.geometry('600x200')
main_window.title('Football')

URL = 'https://www2.laczynaspilka.pl/zawodnik/adrian-pazura,1239302.html'
page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')
minuty = bs.find('div', class_='season__stats-item grid-14 grid-mt-24 grid-msw-48').get_text()
mecze = bs.find('div', class_='season__stats-item grid-10 grid-mt-24 grid-msw-48').get_text()
bramki = bs.find('div', class_='season__stats-item grid-10 item--red grid-mt-24 grid-msw-48 grid-mt-space-0').get_text()
# next = bs.find('div', class_='grid-16 left').get_text()
print(minuty, mecze, bramki)

Minuty = Label(main_window, width=30, text='Minuty na boisku \n ?').grid(row=0, column=0)
Mecze = Label(main_window, width=30, text='Mecze rozegrane \n ?').grid(row=0, column=1)
Bramki = Label(main_window, width=30, text='Strzelone bramki \n ?').grid(row=0, column=2)

address = Entry(main_window, width=35, borderwidth=5)
address.grid(row=3, column=0, columnspan=3, padx=30)


def on_click():
    Label(main_window, width=30, text=minuty).grid(row=0, column=0)
    Label(main_window, width=30, text=mecze).grid(row=0, column=1)
    Label(main_window, width=30, text=bramki).grid(row=0, column=2)


EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  # https://www.youtube.com/watch?v=IolxqkL7cD8 zmienne srodowiskowe WINDOWS
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
# print(EMAIL_PASSWORD, EMAIL_ADDRESS)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)


def send_email():
    msg = EmailMessage()
    msg['Subject'] = 'AKTUALNE WYNIKI'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = address.get()
    msg.set_content(f'Moje aktualne statystyki \n {minuty} {mecze} {bramki}')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


Button(main_window, text="Refresh", command=on_click).grid(row=2, column=2)
Button(main_window, text="EMAIL", command=send_email).grid(row=3, column=2)

main_window.mainloop()
