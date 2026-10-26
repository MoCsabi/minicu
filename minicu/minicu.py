from contextlib import redirect_stdout
from io import StringIO
import types
from google import genai
from google.genai import types
import pyautogui
from PIL import ImageDraw
import platform
from plyer import notification
import minicu.prompt as prompt

def capture_screen_with_cursor():
    screenshot = pyautogui.screenshot()
    mouse_x, mouse_y = pyautogui.position()
    draw = ImageDraw.Draw(screenshot)
    cursor_points = [(mouse_x, mouse_y), (mouse_x + 15, mouse_y + 15), (mouse_x + 5, mouse_y + 18)]
    draw.polygon(cursor_points, fill="red", outline="black")
    draw.ellipse([mouse_x-2, mouse_y-2, mouse_x+2, mouse_y+2], fill="white")
    return screenshot
client = genai.Client()
def main():
    system_prompt= prompt.get_prompt(platform=platform.platform(), size=pyautogui.size())
    chat = client.chats.create(model="gemini-3.5-flash-lite",
                            config=types.GenerateContentConfig(system_instruction=system_prompt, thinking_config=types.ThinkingConfig(thinking_level="HIGH"))
                            )
    screenshot = capture_screen_with_cursor()
    output=""
    user_prompt = input("Prompt:\n")
    response = chat.send_message(
        [user_prompt,screenshot,"OUTPUT: "+output]
    )
    while not response.text.strip().startswith("END"):
        cmd = response.text.rstrip("`").lstrip("`")
        if cmd.startswith("python"): cmd=cmd[len("python"):]
        print(response.text)
        try:
            tmp_stdout = StringIO()
            with redirect_stdout(tmp_stdout):
                exec(cmd)
            output = tmp_stdout.getvalue()
        except Exception as e:
            output=f"ERROR: {e}"
        if output!="": print(f"---\nOutput: {output}\n---")
        screenshot = capture_screen_with_cursor()
        screenshot.save("screenshot.png")
        response=chat.send_message([screenshot,"OUTPUT: "+output])
    print(response.text)
    notification.notify(title='Feladat kész',app_name='Minicu',message='Az ágens végzett az utasítások végrehajtásával.')