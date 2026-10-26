# MiniCU - A stupid(ly) simple computer use agent
Saját Computer Use ágens kevesebb mint 50 sor kódból, ami "bármire képes"
## Absztrakt
Fejlesztettem egy gemini api-t használó minimalista computer use ágenset pythonban. A cél egy minimális működő megoldás létrehozása volt. A kontrol loop úgy épül fel, hogy az ágens kap egy képernyőfotót és egy utasítást, majd a válaszában megad nyers python kódot amit egy exec() blokkban végrehajtódik. A modell használhatja például a pyautogui könyvtárat a géppel való interaktáláshoz, de képes tetszőleges kód végrehajtására, így "bármire képes".
## Próbáld ki
>[!WARNING] Warning
>Semmiképp ne futtasd a saját gépeden! Csakis olyan gépen futtasd ahol azt se bánnád ha az egész rendszert törölné! A következő útmutató ehhez fog segédletet nyújtani

Elérhetővé tettem a projektet a GitHub oldalamon: https://github.com/MoCsabi/minicu  
A kipróbáláshoz én az alábbi folyamatot ajánlom:  
[Szükséges]: `BME eduID`,`Google fiók`
[Röviden]: Létrehunk egy ingyenes VPS-t a BME Smallville-en, amin biztonságosan futtathatjuk a minicu programot. Az AI ágens futtatásához az ingyenes API kulcsot a Google AI Studio-ból szerezzük. 
>[!Warning]
>Az ingyenes API kulccsal együtt jár hogy a beszélgetést (beleértve a képernyőfotókat) a Google felhasználja az AI fejlesztésére, akár emberek is megnézhetik manual review-ként
- ### VPS létrehozása
    - Látogasd meg a [BME Smallville](https://smallville.cloud.bme.hu/) és jelentkezz be a BME eduID-vel.
    - Hozz létre egy új VPS-t (Ubuntu 22.04 LTS Server amd64 + xfce) sablonnal![Image showing template](image.png)
    - Létrehozás után menj a Hálózat menüpontra és nyisd meg a 22/tcp portot a VPS-hez (ez szükséges lesz az SSH kapcsolatra)![image showing connections tab](image-1.png)
    - Miután elindult a szerver csatlakozz rá a `Csatlakozás` gombbal (ha még nem volt telepítve a Circle Client akkor először azt fogja telepíteni)
    - Ha minden jól ment akkor most látod a szerver képernyőjét, tudsz interaktálni vele.
- ### SSH kapcsolat
    - Nyiss egy terminált a gépen és írd be a következő parancsot:
    >sudo systemctl start ssh.service
    - Ez elindította az SSH szervert a VPS-en, a címét a Circle Clientben a `Hálózat` menüpontban találod.
    - Csatlakozz SSH-n a VPS-hez (`ssh`, PuTTY, stb...)! Figyelj hogy a portnak is a `Hálózat` menüpontban megadott portnak kell lennie!
    - Ha minden jól ment akkor most már a terminálban vagy a VPS-en, és a Circle Clientben is látod a VPS képernyőjét.
- ### API kulcs beszerzése
    - Látogasd meg a [Google AI Studio](https://studio.google.com/) oldalt és jelentkezz be a Google fiókoddal.
    - Kattints a kulcs ikonra a alul a fiókod mellett, és másold ki az API kulcsot, vagy csinálj egy újat! Ez teljesen ingyenes, de limitált a használata.
    - Másold ki az API kulcsot, majd a VPS-en a terminálban írd be a következő parancsot hogy a program ismerje majd a kulcsot a környezeti változóból:
    >export GEMINI_API_KEY=IDE_ÍRD_BE_AZ_API_KULCSOT
    - Ezután a program már használhatja az API kulcsot.
- ### Környezet előkészítése
    - A minicu futtatására az ssh kapcsolatban lévő terminált fogjuk használni, így folyton látod mit csinál és le tudod állítani ha kell. A Circle Clientben a VPS képernyőjén pedig látod az ágens által végrehajtott műveleteket.
    - Futtasd a következő parancsot a VPS-en, hogy az ágens tudjon interkatálni a képernyővel:
    >sudo apt install python3-tk python3-dev
    - És hogy tudjon képernyőfotót készíteni:
    >sudo apt install gnome-screenshot
    - Hogy az ssh kapcsolatban lévő terminál a VPS képernyőjét használja:
    >export DISPLAY=:10
    - Ha ez nem működik, próbáld meg a :10 helett a :0-t és az :1-et
- ### Minicu futtatása
    - Először telepítsd `pip`-pel a minicu könyvtárat:
    >pip install git+github.com/MoCsabi/minicu
    - Ezután futtasd a minicu programot, amit a pip alapvetően a `~/.local/bin` könyvtárba telepít, így a következő parancsot írd be:
    >~/.local/bin/minicu
    - Ha minden jól ment akkor most megjelenik a terminálban a `Prompt:` felirat, ide írd be az utasítást amit az ágensnek végre kell hajtania.
    - Majd nyomj entert, és nézd ahogy az ágens végrehajtja a műveleteket a VPS képernyőjén. Ha valami olyat csinál amit nem szeretnél, nyomj Ctrl+C-t a terminálban és az ágens leáll.
## Az ötlet
Először ki akartam próbálni egy már létező megoldást a szorgalmi keretében. Azonban amikor telepítettem meglepődve láttam, hogy ez egy python script. Laikusként azt gondoltam hogy ezek a computer use ágensek brutális keretrendszereket használnak és nagy cégek fejlesztik. Ekkor jött az ötlet, hogy lehet nem is kell olyan bonyolultnak lennie, sőt, lehet kifejezetten egyszerű is.
## A prototípus
A cél az volt, hogy legyen egy teknikailag működő megoldásom. Két kihívás volt: az ágensnek "látnia kell", és képesnek kell lennie egy felhasználóhoz hasonló művelteket végrehajtani. Az elsőre a megoldás képernyőfotók küldése volt, a másodikra pedig a python "zseniális" `exec()` blokkja jelentette a megoldást. Így az ágens végrehajthat felhasználói műveleteket pl a `pyautogui` könyvtárral, de ami a kedvencem, tetszőleges kódot hajt végre, tehát "bármire képes". Például képes rendszerhívásokat végezni vagy saját szkriptet írni feladatok végrehajtására.     
A legegyszerűbb verzió így nézett ki:  
```python
from google import genai
import pyautogui
client = genai.Client()
chat = client.chats.create(model="gemini-3.5-flash-lite",
                           config=types.GenerateContentConfig(system_instruction="Egy computer use ágens vagy. A feladatod hogy végrehajtsd a kért műveletet python kód írásával. A válaszod egy python exec blockban végre lesz hajtva. Utána kapsz egy képernyőfotót az új állapotról, ahol újabb műveleteket hajthatsz végre. Ha kész vagy írj annyit, hogy END, minden formázás nélkül.", thinking_config=types.ThinkingConfig(thinking_level="HIGH"))
                        )
screenshot = pyautogui.screenshot()
response = chat.send_message(
    ["Küldj a barátomnak egy discord üzentet!",screenshot]
)
while not response.text=="END":
    print(response.text)
    exec(response.text)
    screenshot = pyautogui.screenshot()
    response=chat.send_message([screenshot])
```
Ez a kevesebb mint 10 soros kód már teljesen működőképes volt, ami szerintem csodálatos.
### Működés
A szkript létesít egy kapcsolatot a gemini api-val a GEMINI_API_KEY környezeti változót használva. A szkript létrehoz egy chatet a gemini-3.5-flash-lite modellel, és megadja neki a rendszer promptot, ami leírja a feladatát. Ezután készít egy képernyőfotót a pyautogui könyvtár segítségével, majd elküldi a feladatot és a képernyőfotót a modellnek. A modell válaszában python kódot ad vissza, amit az exec() függvény segítségével végrehajtunk. Ezután újra készítünk egy képernyőfotót, hogy az ágens lássa az eredményt. A folyamat addig ismétlődik, amíg az ágens nem írja be az "END" szót, jelezve, hogy befejezte a feladatot.  
## Problémák
Számomra az egész projekt legérdekesebb része a gyengeségek/problémák felfedezése volt. Egyedi belelátást adott a computer use kihívásaira, érdekes volt megfigyelni hogy a hibák többsége egy valós probléma, amivel sokan foglalkoztak, és mégérdekesebb volt a létező megoldások megértése.
### Megfelelő visszacsatolás
Sokat fejlődött a modell attól, hogy több adatot kapott visszacsatolásként. A szkriptjeinek a kimenetét/error-jait visszaküldöm neki mert észrevettem hogy gyakran ír a kimenetre viszont azt utána nem látja. Egy másik helyzet ahol a megfelelő visszacsatolás segített az egér helyzete volt. Ugyanis kiderült hogy a képernyőfotókon nincs rajta az egér, így amikor melléklikkel nem tud javítani.
### Klikkelési pontatlanság
Ez volt a legérdekesebb probléma amivel találkoztam. Kiderült, hogy a legtöbb AI chatbot egyszerűen nem tudja megmondani hogy egy képen egy gomb milyen x,y koordinátán van. Egyrészt nem erre lettek trainelve, másrészt a képeket felbontják chunkokra, durva tömörítést alkalmazva hogy kevesebb token legyen.  
Kiderült, hogy segít ha egy "0-1000 normalizált bounding box"-ot kérek a cél gomb köré, majd ebből számol koordinátát és nem rögtön koordinátát. Ez azért van mert erre valamilyen szinten lett tanítva. Tovább segített hogy angolra fordítottam a szöveget, hogy méginkább ráismerjen a kulcsszavakra. Ezt úgy valósítottam meg, hogy egy kommentbe írja le a bounding boxot majd abból python kóddal számolja ki a középpontot. Nagyon meglepett, de ez tényleg segített (bár továbbra is elég béna).  
A profi ágensek erre külön erre tanított ún. "grounding modell"-t használnak aminek pont annyi a feladata hogy képről felismerje hol van a cél gomb. Ez együtt dolgozik a valódi végrehajtó ágenssel.
### Klikkelési pontatlanság part 2
A klikkelési gyengesége fényt vet egy nagyobb problémára: miért kell klikkelnie?  
Sokkal hatékonyabban megoldhatná a feladatokat programkód futtatásával, rendszerhívásokkal vagy billentyűkombinációkkal. Az utóbbi nem lenne rossz ötlet, mivel a legtöbb applikáció támogatja az accessibility feature-öket, legtöbbször klikkelés nélkül használható az alkalmazás. Beleírtam a promptba hogy ezeket a megoldásokat részesítse előnyben.  
Szerintem itt egy általánosabb tanulság is levonható ebből: miért kell a computer use ágenseknek klikkelnie? Persze az a cél, hogy képes legyen user-szinten interaktálni az operációs rendszerrel, de ezt szerintem csak végszükség esetén kéne használni.
### Ingyenes API kulcs
Az, hogy ingyenes API kulcsot használunk a modellhez két hátránnyal jár:  
- Egyrészt durva limitek vannak, így tényleg csak egy proof of concept megoldásra jó, de inkább az a zavaró, hogy így nem élvezünk prioritást, amikor terheltek a szerverek nagyon lassan érkezik válasz.
- Másrészt az ingyenes kulcs használattak együtt jár hogy az adataid (jelen esetben képernyőképek a gépről) egyenesen vissza mennek a Google-nek, akár emberek is megtekinthetik manual review-re.
## Reflekció
A célom ezzel a projekttel enm az volt, hogy egy "jó" computer use ágenset fejlesszek, amit mások használnának. Nem is gondolom, hogy ezt elértem. Rengeteg megoldatlan probléma maradt. A cél az volt hogy tanuljak, és minél egyszerűbb megoldást találjak, amit szerintem el is értem. A fejlesztett verzió megtalálható a https://github.com/MoCsabi/minicu linken. A forráskód továbbra is 50 sor kód alatt van!
### Tesztek
A fejlesztés során rengeteget teszteltem. Ez a lezáró fejezet összegyűjti a legérdekesebb dolgokat amiket csinált.  
- Egyszer átírta a saját forráskódját (feltehetőleg véletlenül) majd kiadta a git revert utasítást hogy sikeresen visszaállítsa
- Sokszor bezárta a saját terminálját
- Sikerült discordon ráírnia a barátomra (csak 2 másik emberre írt rá előtte)