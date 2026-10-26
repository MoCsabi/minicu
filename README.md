# MiniCU - A stupid(ly) simple computer use agent
Saját Computer Use ágens kevesebb mint 50 sor kódból, ami "bármire képes"
## Absztrakt
Fejlesztettem egy gemini api-t használó minimalista computer use ágenset pythonban. A cél egy minimális működő megoldás létrehozása volt. A kontrol loop úgy épül fel, hogy az ágens kap egy képernyőfotót és egy utasítást, majd a válaszában megad nyers python kódot amit egy exec() blokkban végrehajtódik. A modell használhatja például a pyautogui könyvtárat a géppel való interaktáláshoz, de képes tetszőleges kód végrehajtására, így "bármire képes".
## Működés
>[!WARNING] Warning
>Semmiképp ne futtasd a saját gépeden!

Elérhetővé tettem a projektet a GitHub oldalamon: TODO ADD  
TODO telepítés
TODO free api key
TODO javasolni vps-t (circle)
TODO használati guide
TODO best practice: be ssh-zni+rdesktop vagy vm

## Az ötlet
Először ki akartam próbálni egy már létező megoldást a szorgalmi keretében. Nagyon meglepődtem amikor láttam, hogy az eszköz amit tesztelni akartam egy python szkript. Én azt hittem hogy ezek a computer use programok valami géphez közelibb, komoly keretrendszerben íródtak. Ezután jött az ötlet, hogy lehet, hogy nem is olyan megfoghatatlanok ezek a szoftverek.
## A prototípus
A cél az volt, hogy legyen egy teknikailag működő megoldásom. A legegyszerűbb verzió így nézett ki:  
```python
from google import genai
import pyautogui
client = genai.Client()
chat = client.chats.create(model="gemini-3.5-flash-lite",
                           config=types.GenerateContentConfig(system_instruction="Egy computer use ágens vagy. A feladatod hogy végrehajtsd a kért műveletet python kód írásával. A válaszod egy python exec blockban végre lesz hajtva. Utána kapsz egy képernyőfotót az új állapotról, ahol újabb műveleteket hajthatsz végre. Ha kész vagy írj annyit, hogy END, minden formázás nélkül.", thinking_config=types.ThinkingConfig(thinking_level="HIGH"))
                        )
screenshot = pyautogui.screenshot()
response = chat.send_message(
    ["IDE ÍRD A FELADATOT",screenshot]
)
while not response.text=="END":
    print(response.text)
    exec(response.text)
    screenshot = pyautogui.screenshot()
    response=chat.send_message([screenshot,"OUTPUT: "+output])
```
Ez a kevesebb mint 10 soros kód már technikailag működőképes volt!
### Működés
A szkript létesít egy kapcsolatot a gemini api-val. Ez alapból a GEMINI_API_KEY környezeti változót használja.
TODO finish short desc
## Problémák
TODO biztonsági flaw (free api)
TODO biztonsági flaw (elront valamit, prompt injection)
TODO nem tud klikkelni
TODO lassu response
## Megoldások
TODO én mit csináltam
TODO profik mit csinálnak (tool calling stb)
## Reflekció
TODO a lényeg nem egy "jó" szoftver, inkább vicces/POC
TODO mit tanultam
TODO AI használata a dokumentumban
### Tesztek
TODO miket csinált ami vicces (discord rossz embernek ír, kilőtte magát, átírta a forrsákódját majd git revert-elt, SSHétfő)