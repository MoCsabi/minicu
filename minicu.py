from contextlib import redirect_stdout
from io import StringIO
from time import sleep
import types

from google import genai
from google.genai import types
import pyautogui
import pyautogui
from PIL import ImageDraw
import platform

def capture_screen_with_cursor():
    screenshot = pyautogui.screenshot()
    mouse_x, mouse_y = pyautogui.position()
    draw = ImageDraw.Draw(screenshot)
    cursor_points = [(mouse_x, mouse_y), (mouse_x + 15, mouse_y + 15), (mouse_x + 5, mouse_y + 18)]
    draw.polygon(cursor_points, fill="red", outline="black")
    draw.ellipse([mouse_x-2, mouse_y-2, mouse_x+2, mouse_y+2], fill="white")
    return screenshot
client = genai.Client()
chat = client.chats.create(model="gemini-3.5-flash-lite",
                           config=types.GenerateContentConfig(system_instruction=f"Egy computer use agent vagy. {platform.system()} operációs rendszeren futsz, a képernyő felbontása {pyautogui.size()}. Kapsz egy képernyőfotót, és egy feladat promptot, majd a válaszod lefut egy python exec() blokkban. Ezen felül megkapod a múltkori futásod kimenetét, error-jait! Nyers kódot küldj vissza! Használhatod a pyautogui-t vagy akár syscallokat! CSAKIS akkor klikkelj ha NINCS más megoldás! Minden esetben használj helyette billentyű kombinációkat! Mielőtt teszel valami nagy hatásút (elküldesz üzenetet, törölsz filet) várj az akció végrehajtásával amíg nem kapsz egy képernyőfotót amin megbizonyosulhatsz hogy minden rendben van, és ha így van hajtsd végre! " \
                           "Ha végeztél, minden esetben ellenőrizd hogy megfelelő állapotban van-e hagyva. Ezt szükség esetén egy üres python script-el teheted meg (pass utasítás). Ha erről megbizonyosodtál, írd hogy END, minden formázás nélkül egy új üzenetben, ne python script mögé csatolva. Az utolsó üzenet elküldése előtt írj egy pár mondatos összefoglalót a munkádról, mi okozott nehézséget, mi alapján döntöttél, milyen bemenet volt hasznos/nem hasznos!", thinking_config=types.ThinkingConfig(thinking_level="HIGH"))
                        )
screenshot = capture_screen_with_cursor()
output=""
response = chat.send_message(
    ["Nyisd meg a discordot és navigálj a papagájos szerver #secret csatornájába!",screenshot,"OUTPUT: "+output]
)
while response.text.strip()!="END":
    cmd = response.text.rstrip("`").lstrip("`")
    if cmd.startswith("python"): cmd=cmd[len("python"):]
    print(response.text)
    sleep(1)
    try:
        tmp_stdout = StringIO()
        with redirect_stdout(tmp_stdout):
            exec(response.text)
        output = tmp_stdout.getvalue()
    except Exception as e:
        output=f"ERROR: {e}"
    screenshot = capture_screen_with_cursor()
    screenshot.save("screenshot.png")
    while True:
        try:
            response=chat.send_message(
                [screenshot,"OUTPUT: "+output]
            )
            break
        except:pass