import requests

def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果响应状态码不是200,则抛出异常
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

def main():
    url = "http://192.168.3.87:8200/cdkey/?cd_key=74624342-cb5c-455a-857b-f785515dca89"
    response, error_text = make_request(url)
    if response:
        print("Server response:", response)
        if 'expires_at' in response:
            print("Expire Time:", response['expires_at'])
    if error_text:
        print("Error text:", error_text)

if __name__ == "__main__":
    main()
