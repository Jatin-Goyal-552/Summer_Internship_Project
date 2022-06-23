import requests

url = "https://summerinternshipproject.pythonanywhere.com/code/"

payload={'code_text': 'hello',
'code_time': '30',
'question_time': '60'}
files=[
  ('code_image',('photo2.jpg.jpeg',open('C:/Users/LENOVO/Downloads/photo2.jpg.jpeg','rb'),'image/jpeg'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
