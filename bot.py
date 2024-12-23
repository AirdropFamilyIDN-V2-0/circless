import requests
import json
import time

def banner():
    print("===================================")
    print("     Auto Reff waitlist circless   ")
    print("          @AirdropFamilyIDN        ")
    print("===================================")

url = "https://audience-consumer-api.zootools.co/v3/lists/UZiEmVdANl6A8rLJCDhb/members"

headers = {
    "Authorization": "Bearer",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Origin": "https://form.zootools.co",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Accept-Language": "en-GB,en;q=0.9",
    "Sec-CH-UA": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}

payload = {
    "utmSource": "",
    "utmMedium": "",
    "utmCampaign": "",
    "utmTerm": "",
    "utmContent": "",
    "pageReferrer": "",
    "email": "",
    "twitter": "",
    "hiddenFields": {
        "productId": "",
        "projectId": "",
        "teamId": "",
        "userId": ""
    },
    "captchaToken": "",
    "referral": ""
}

try:
    banner()
    
    api_key = input("Masukkan API Key 2captcha.com: ")
    referral_code = input("Masukkan kode referral (contoh: 7OpYRNViOvMHs0Ocnehf): ")
    iterations = int(input("Masukkan jumlah reff: "))
    payload["referral"] = referral_code

    def get_random_user():
        response = requests.get("https://randomuser.me/api/")
        if response.status_code == 200:
            user_data = response.json()['results'][0]
            email_username = user_data['email'].split('@')[0]
            username = user_data['login']['username']
            return f"{email_username}@gmail.com", username
        else:
            raise Exception("Failed to fetch random user data")

    for _ in range(iterations):
        random_email, random_username = get_random_user()

        payload["email"] = random_email
        payload["twitter"] = f"@{random_username}"

        def get_turnstile_token(api_key, sitekey, site_url):
            data = {
                'key': api_key,
                'method': 'turnstile',
                'sitekey': sitekey,
                'pageurl': site_url
            }
            response = requests.post('http://2captcha.com/in.php', data=data)
            print("CAPTCHA REQUEST :", response.text)
            captcha_id = response.text.split('|')[1]

            result_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
            max_attempts = 12  # Maksimal 12 kali percobaan (2 menit)
            attempts = 0

            while attempts < max_attempts:
                result_response = requests.get(result_url)
                if 'CAPCHA_NOT_READY' in result_response.text:
                    print("CAPTCHA belum siap, menunggu 10 detik...")
                    time.sleep(10)
                    attempts += 1
                    continue
                return result_response.text.split('|')[1]

            raise Exception("Gagal mendapatkan token CAPTCHA setelah beberapa percobaan")

        captcha_token = get_turnstile_token(
            api_key=api_key,
            sitekey="0x4AAAAAAABCOgX4x6RvmA0a",
            site_url=f"https://form.zootools.co/go/UZiEmVdANl6A8rLJCDhb?ref={referral_code}"
        )

        payload["captchaToken"] = captcha_token

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            
            print("Response:", response.text)
            print("")
            print("Reff sukses")
            print(f"Member Email: {response_data['member']['email']}")
            print(f"Member ID: {response_data['member']['id']}")
            print(f"Status: {response_data['member']['status']}")
            print("===================================")
            time.sleep(5)
        else:
            print(f"Failed to make the request. Status Code: {response.status_code}")
            print("Response:", response.text)

except KeyboardInterrupt:
    print("\nTerminated by user")
