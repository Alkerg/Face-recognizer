import pyautogui as pg, webbrowser as wb, time as tm

#------------------FUNCTION THAT SEND MESSAGES VIA WHATSAPP----------------------
countW = 0
def enviar_whatsapp(persona,numero):
    global countW
    if countW < 1:
        wb.open("https://web.whatsapp.com/send?phone=+51" + numero)
        tm.sleep(8)
        pg.write("¡ALERTA! " + persona + " esta afuera de tu casa")
        pg.press("enter")
        countW += 1
        return
    else:
        pass
        