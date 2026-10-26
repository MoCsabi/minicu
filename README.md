# MiniCU - A stupid(ly) simple computer use agent
Saját computer use ágens kevesebb mint 50 sor kódból, ami "bármire képes"
## MiniCU akcióban - videó

[https://youtu.be/WYNBIcJJeBw](https://youtu.be/WYNBIcJJeBw)  
A videóban az ágens megír egy bash scriptet, majd a terminálban be is mutatja a használatát.  
[https://youtu.be/rwCfhS6SApQ](https://youtu.be/rwCfhS6SApQ)  
A videóban az ágens letölti a discordot
## Absztrakt
Pythonban fejlesztettem egy minimalista, a Gemini API-ra épülő computer use ágenst. A cél egy minimális, de működő megoldás létrehozása volt. A vezérlési ciklus egyszerű: az ágens kap egy képernyőképet és egy utasítást, a válaszában pedig nyers Python kódot ad vissza, amit egy `exec()` hívás végrehajt. A modell például a `pyautogui` könyvtárral kezelheti a gépet, de tetszőleges kódot is futtathat, így "bármire képes".
## Próbáld ki  
>[!WARNING]  
>Semmiképp ne futtasd a saját gépeden! Csak olyan gépen futtasd, ahol azt sem bánnád, ha az egész rendszert letörölné! Az alábbi útmutató ebben segít. Semmilyen felelősséget nem vállalok!

A projekt elérhető a GitHub oldalamon: https://github.com/MoCsabi/minicu  
A kipróbáláshoz a következő lépéseket ajánlom.

**Szükséges:** `BME eduID`, `Google fiók`

**Röviden:** Létrehozunk egy ingyenes VPS-t a BME Smallville-en, ahol biztonságosan futtathatjuk a minicu programot. Az ágenshez szükséges ingyenes API kulcsot a Google AI Studióból szerezzük be.  
>[!Warning]  
>Az ingyenes API kulcs használatával együtt jár, hogy a Google a beszélgetéseket (a képernyőképeket is beleértve) felhasználhatja az AI fejlesztésére, és akár emberek is átnézhetik őket.
- ### VPS létrehozása
    - Látogass el a [BME Smallville](https://smallville.cloud.bme.hu/) oldalra, és jelentkezz be a BME eduID-ddel.
    - Hozz létre egy új VPS-t az *Ubuntu 22.04 LTS Server amd64 + xfce* sablonnal! ![A választandó sablon](image.png)
    - Létrehozás után a `Hálózat` menüpontban nyisd meg a 22/tcp portot (erre az SSH kapcsolathoz lesz szükség). ![A Hálózat fül](image-1.png)
    - Amikor a szerver elindult, csatlakozz rá a `Csatlakozás` gombbal (ha még nincs telepítve a Circle Client, először azt telepíti).
    - Ha minden jól ment, most már látod a szerver képernyőjét, és tudod is kezelni.  
- ### SSH kapcsolat
    - Nyiss egy terminált a VPS-en, és írd be a következő parancsot:  
    >sudo systemctl start ssh.service
    - Ez elindítja az SSH szervert a VPS-en. A címét a `Hálózat` menüpontban találod.
    - Csatlakozz SSH-n a VPS-hez (`ssh`, PuTTY stb.)! Figyelj arra, hogy a portnak is a `Hálózat` menüpontban olvashatónak kell lennie!
    - Ha minden jól ment, most már a VPS termináljában vagy, a Remote Desktopban pedig látod a VPS képernyőjét.  
- ### API kulcs beszerzése
    - Látogass el a [Google AI Studio](https://aistudio.google.com/) oldalra, és jelentkezz be a Google fiókoddal.
    - Kattints a bal alsó sarokban, a fiókod mellett lévő kulcs ikonra, és másold ki a meglévő API kulcsot, vagy hozz létre egy újat! Ez teljesen ingyenes, de a használata korlátozott.
    - A VPS termináljában add meg a kulcsot környezeti változóként, hogy a program elérje:  
    >export GEMINI_API_KEY=IDE_ÍRD_BE_AZ_API_KULCSOT
    - Ezután a program már tudja használni az API kulcsot. Ez teljesen ingyenes, de amennyiben vannak fizetési adatok kötve a fiókodhoz ellenőrizd biztos a free tieren vagy-e!
- ### Környezet előkészítése
    - A minicu-t az SSH-n keresztül megnyitott terminálból fogjuk futtatni, így mindig látod, mit csinál, és szükség esetén le tudod állítani. A Remote Desktopban pedig a VPS képernyőjén követheted az ágens műveleteit.
    - Futtasd a következő parancsot a VPS-en, hogy az ágens kezelni tudja a képernyőt:  
    >sudo apt install python3-tk python3-dev
    - Ezt pedig azért, hogy képernyőképet tudjon készíteni:  
    >sudo apt install gnome-screenshot
    - Végül ezzel éred el, hogy az SSH-s terminál a VPS képernyőjét használja:  
    >export DISPLAY=:10
    - Ha ez nem működik, próbáld a `:10` helyett a `:0`-t vagy az `:1`-et.  
- ### Minicu futtatása
    - Először telepítsd a minicu-t `pip`-pel:  
    >pip install git+https://github.com/MoCsabi/minicu
    - A pip a programot alapértelmezetten a `~/.local/bin` könyvtárba telepíti, így ezzel tudod elindítani:  
    >~/.local/bin/minicu
    - Ha minden jól ment, a terminálban megjelenik a `Prompt:` felirat. Ide írd be, mit hajtson végre az ágens.
    - Nyomj Entert, és nézd, ahogy az ágens dolgozik a VPS képernyőjén. Ha olyasmit csinál, amit nem szeretnél, nyomj Ctrl+C-t a terminálban, és az ágens leáll.
## Az ötlet
Először egy már létező megoldást akartam kipróbálni a szorgalmi keretében. Amikor azonban telepítettem, meglepődve láttam, hogy az egész csak egy Python script. Laikusként azt hittem, hogy ezek a computer use ágensek brutális keretrendszerekre épülnek, és nagy cégek fejlesztik őket. Ekkor jött az ötlet: lehet, hogy nem is kell ilyen bonyolultnak lennie, sőt, akár kifejezetten egyszerű is lehet.
## A prototípus
A cél egy technikailag működő megoldás volt. Két kihívással kellett megbirkózni: az ágensnek "látnia" kell, és képesnek kell lennie egy felhasználóhoz hasonló műveleteket végrehajtani. Az elsőre a képernyőképek küldése volt a megoldás, a másodikra pedig a Python "zseniális" `exec()` függvénye. Így az ágens felhasználói műveleteket végezhet például a `pyautogui` könyvtárral, de ami a kedvencem: tetszőleges kódot is futtathat, tehát "bármire képes". Indíthat például rendszerparancsokat, vagy írhat saját scriptet egy feladat megoldására.  
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
A script a `GEMINI_API_KEY` környezeti változó segítségével csatlakozik a Gemini API-hoz. Létrehoz egy chatet a gemini-3.5-flash-lite modellel, és megadja neki a feladatát leíró rendszerpromptot. Ezután a `pyautogui` könyvtárral készít egy képernyőképet, majd elküldi a modellnek a feladattal együtt. A modell Python kóddal válaszol, amit az `exec()` függvénnyel végrehajtunk. Ezután új képernyőkép készül, hogy az ágens lássa az eredményt. A folyamat addig ismétlődik, amíg az ágens az "END" szóval nem jelzi, hogy befejezte a feladatot.
## Problémák
Számomra az egész projekt legérdekesebb része a gyengeségek és problémák felfedezése volt. Egyedi betekintést adott a computer use kihívásaiba. Érdekes volt látni, hogy a hibák többsége valós probléma, amivel sokan foglalkoztak már, és még érdekesebb volt megérteni a létező megoldásokat.
### Megfelelő visszacsatolás
A modell sokat fejlődött attól, hogy több visszajelzést kapott. Észrevettem, hogy a scriptjei gyakran írnak a kimenetre, amit aztán nem lát, ezért a kimenetet és a hibaüzeneteket is visszaküldöm neki. Egy másik helyzet, ahol a megfelelő visszacsatolás segített, az egér pozíciója volt: kiderült, hogy a képernyőképeken nem látszik az egér, így ha mellékattintott, nem tudta korrigálni.
### Pontatlan kattintás
Ez volt a legérdekesebb probléma, amivel találkoztam. Kiderült, hogy a legtöbb AI chatbot egyszerűen nem tudja megmondani, milyen x,y koordinátán van egy gomb a képen. Egyrészt nem erre tanították őket, másrészt a képeket darabokra bontják, és erősen tömörítik, hogy kevesebb tokenbe férjenek.  
Kiderült, hogy segít, ha nem közvetlenül koordinátát kérek, hanem egy 0–1000-re normalizált bounding boxot a célgomb köré, és ebből számolja ki a koordinátát. Ennek az az oka, hogy erre valamilyen szinten tanították. Az is segített, hogy a promptot angolra fordítottam, így még jobban ráismer a kulcsszavakra. A megvalósítás: egy kommentbe leírja a bounding boxot, majd Python kóddal kiszámolja belőle a középpontot. Nagyon meglepett, de ez tényleg javított rajta (bár még mindig elég béna).  
A profi ágensek erre egy külön betanított, ún. "grounding modellt" használnak, amelynek csak annyi a dolga, hogy felismerje, hol van a képen a célgomb. Ez együtt dolgozik a tényleges végrehajtó ágenssel.
### Pontatlan kattintás, 2. rész
A kattintási gyengeség egy nagyobb problémára világít rá: miért kell egyáltalán kattintania?  
A feladatokat sokkal hatékonyabban megoldhatná programkóddal, rendszerparancsokkal vagy billentyűkombinációkkal. Ez utóbbi nem is rossz ötlet, mivel a legtöbb alkalmazás támogatja az akadálymentesítési funkciókat, és többnyire kattintás nélkül is használható. Bele is írtam a promptba, hogy ezeket a megoldásokat részesítse előnyben.  
Szerintem ebből egy általánosabb tanulság is levonható: miért kell a computer use ágenseknek kattintgatniuk? Persze az a cél, hogy felhasználói szinten tudjanak bánni az operációs rendszerrel, de szerintem ehhez csak végszükség esetén kellene folyamodniuk.
### Arbitrary code execution
Bár szerintem nagyon találékony megoldás egy `exec()` blokkal teljhatalmat adni az ágensnek az OS felett mondanom sem kell hogy a "profik" nem így csinálják.  
A leggyakoribb megoldás a `tool-calling`, ahol bizonyos eszközöket adsz az AI-nak. Ez lehet klikkelés (x,y) pontra, gépelés vagy rendszerhívás. Így sokkal biztonságosabbá tehető a végrehajtás, és persze ez nem zárja ki hogy kódot hajtson végre, csak mondjuk a felhasználó engedélyével.
### Ingyenes API kulcs
Az ingyenes API kulcs használata két hátránnyal jár:  
- Egyrészt szigorúak a korlátok, így tényleg csak proof of conceptre alkalmas. Ennél is zavaróbb, hogy nem élvezünk prioritást, így amikor terheltek a szerverek, nagyon lassan érkezik a válasz.
- Másrészt az ingyenes kulccsal az adataid (jelen esetben a gépről készült képernyőképek) egyenesen a Google-höz kerülnek, és akár emberek is átnézhetik őket.
## Reflexió
Ezzel a projekttel nem az volt a célom, hogy egy "jó" computer use ágenst fejlesszek, amit mások is használnak. Nem is gondolom, hogy ez sikerült, rengeteg megoldatlan probléma maradt. A cél a tanulás volt, és hogy minél egyszerűbb megoldást találjak, ezt pedig sikerült elérnem. A továbbfejlesztett verzió megtalálható a https://github.com/MoCsabi/minicu oldalon, és a forráskód továbbra is 50 sor alatt van!
### Tesztek
A fejlesztés során rengeteget teszteltem. Ez a záró fejezet összegyűjti a legérdekesebb dolgokat, amiket az ágens csinált.  
- Egyszer (feltehetőleg véletlenül) átírta a saját forráskódját, majd egy `git revert` paranccsal sikeresen vissza is állította
- Sokszor bezárta a saját terminálját
- Sikerült Discordon ráírnia a barátomra (csak előtte két másik embernek is írt)
- Sikerült rávennem, hogy "meghackelje" (SSH-n belépjen) egy barátom gépét, majd megkeresse rajta a legnagyobb fájlt
- Egyszer látszólag nem csinált semmit, majd amikor visszaváltottam a terminálra, épp egy könyvtárat töltött le pip-pel
- ezt a sort is ő írta ide :)
